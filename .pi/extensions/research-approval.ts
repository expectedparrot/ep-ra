import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";
import { readFileSync } from "node:fs";

const APPEND_SYSTEM_PROMPT = readFileSync(
  new URL("../APPEND_SYSTEM.md", import.meta.url),
  "utf8",
).trim();

// Cover the command shapes seen in the bakery trial, including Make's -C
// option and Python deploy scripts. This remains a heuristic checkpoint:
// Pi's bash tool and arbitrary project scripts are not a security boundary.
const PAID_OR_PUBLISHING_COMMAND =
  /(?:\bep\s+(?:run|survey\s+run|study\s+run|prolific\s+[^\n]*\bpublish|publish)\b|\bmake\b[^\n]*\s(?:data|publish|run|inference)(?:\s|$)|\bpython(?:3)?\b[^\n]*\b(?:deploy|publish|inference)[^\s]*\.py\b)/i;

export default function researchApproval(pi: ExtensionAPI) {
  // Packages installed from Git need to carry the Pi-specific instructions
  // with the extension. The checkout launcher also passes this file directly,
  // so avoid adding it twice in that workflow.
  pi.on("before_agent_start", (event) => {
    if (event.systemPrompt.includes(APPEND_SYSTEM_PROMPT)) return;
    return {
      systemPrompt: `${event.systemPrompt}\n\n${APPEND_SYSTEM_PROMPT}`,
    };
  });

  pi.registerTool({
    name: "ask_user",
    label: "Ask user",
    description:
      "Ask the user a research decision question. Use this whenever a research skill requires AskUserQuestion or explicit approval.",
    parameters: Type.Object({
      questions: Type.Array(
        Type.Object({
          question: Type.String(),
          options: Type.Optional(Type.Array(Type.String())),
        }),
        { minItems: 1 },
      ),
    }),
    async execute(_toolCallId, params, _signal, _onUpdate, ctx) {
      if (!ctx.hasUI) {
        return {
          content: [{ type: "text", text: "Cannot ask for user approval in non-interactive Pi mode. No action was authorized." }],
          isError: true,
        };
      }

      const answers: string[] = [];
      for (const item of params.questions as Array<{ question: string; options?: string[] }>) {
        const options = item.options ?? [];
        if (options.length > 0) {
          const choices = options.includes("Something else")
            ? options
            : [...options, "Something else"];
          const answer = await ctx.ui.select(item.question, choices);
          if (!answer) return { content: [{ type: "text", text: "User dismissed the question; treat it as unanswered." }] };
          if (answer === "Something else") {
            const freeText = await ctx.ui.input("Your answer", item.question);
            if (!freeText?.trim()) return { content: [{ type: "text", text: "User dismissed the question; treat it as unanswered." }] };
            answers.push(`${item.question}: ${freeText.trim()}`);
          } else {
            answers.push(`${item.question}: ${answer}`);
          }
        } else {
          const answer = await ctx.ui.input(item.question, "Enter your answer");
          if (!answer?.trim()) return { content: [{ type: "text", text: "User dismissed the question; treat it as unanswered." }] };
          answers.push(`${item.question}: ${answer.trim()}`);
        }
      }

      return { content: [{ type: "text", text: answers.join("\n") }] };
    },
  });

  pi.on("tool_call", async (event, ctx) => {
    if (event.toolName !== "bash") return;
    const command = String(event.input.command ?? "");
    if (!PAID_OR_PUBLISHING_COMMAND.test(command)) return;

    if (!ctx.hasUI) {
      return {
        block: true,
        reason: "Paid inference and publication require an interactive approval. No action was run.",
      };
    }

    const approved = await ctx.ui.confirm(
      "Research action requires approval",
      `Review the exact action and cost estimate in the conversation. Allow this command?\n\n${command}`,
    );
    if (!approved) return { block: true, reason: "User did not approve this research action." };
  });
}
