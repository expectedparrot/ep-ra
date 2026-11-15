import type { ExtensionAPI, ExtensionContext } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";
import { readFileSync, statSync } from "node:fs";
import { spawn } from "node:child_process";
import { isAbsolute, resolve } from "node:path";
import { Container, ScrollView, Text } from "@earendil-works/pi-tui";

const CORE_SYSTEM_PROMPT = readFileSync(
  new URL("../../research_agent/skills/workflow-session-start/references/agent-core.md", import.meta.url),
  "utf8",
).trim();
const PI_SYSTEM_PROMPT = readFileSync(
  new URL("../APPEND_SYSTEM.md", import.meta.url),
  "utf8",
).trim();
const APPEND_SYSTEM_PROMPT = `${CORE_SYSTEM_PROMPT}\n\n${PI_SYSTEM_PROMPT}`;

function openWithSystemViewer(path: string): Promise<boolean> {
  const opener = process.platform === "darwin" ? "open" : "xdg-open";
  return new Promise((resolveOpen) => {
    let settled = false;
    let timeout: ReturnType<typeof setTimeout> | undefined;
    const finish = (opened: boolean) => {
      if (settled) return;
      settled = true;
      if (timeout) clearTimeout(timeout);
      resolveOpen(opened);
    };

    const child = spawn(opener, [path], { detached: true, stdio: "ignore" });
    child.once("error", () => finish(false));
    child.once("exit", (code) => finish(code === 0));
    timeout = setTimeout(() => finish(true), 2000);
    child.unref();
  });
}

async function showPresentedFile(path: string, title: string, ctx: ExtensionContext) {
  if (!ctx.hasUI) return;

  const absolutePath = isAbsolute(path) ? path : resolve(path);
  let size: number;
  try {
    size = statSync(absolutePath).size;
  } catch {
    ctx.ui.notify(`Could not open presented file: ${absolutePath}`, "warning");
    return;
  }
  if (size === 0) {
    ctx.ui.notify(`Presented file is empty: ${absolutePath}`, "warning");
    return;
  }
  if (await openWithSystemViewer(absolutePath)) {
    ctx.ui.notify(`Opened ${title} in your system viewer.`, "info");
    return;
  }
  ctx.ui.notify("Could not launch the system viewer; showing text in Pi when possible.", "warning");
  if (size > 2_000_000) {
    ctx.ui.notify(`Presented file is too large for Pi's viewer: ${absolutePath}`, "warning");
    return;
  }

  let contents: Buffer;
  try {
    contents = readFileSync(absolutePath);
  } catch {
    ctx.ui.notify(`Could not read presented file: ${absolutePath}`, "warning");
    return;
  }
  if (contents.includes(0)) {
    ctx.ui.notify(`Pi can show text files in its viewer. File: ${absolutePath}`, "info");
    return;
  }

  const body = new ScrollView(new Text(contents.toString("utf8"), 1, 0), {
    axis: "vertical",
    scrollbar: "auto",
    overscroll: "contain",
  });
  await ctx.ui.custom<void>((tui, theme, keybindings, done) => {
    const container = new Container();
    container.addChild(new Text(theme.fg("accent", theme.bold(title)), 1, 0));
    container.addChild(new Text(theme.fg("dim", absolutePath), 1, 0));
    container.addChild(body);
    container.addChild(new Text(theme.fg("dim", "Use the mouse wheel or arrow keys to scroll; Enter or Esc closes."), 1, 0));
    return {
      render: (width: number) => container.render(width),
      invalidate: () => container.invalidate(),
      handleInput: (data: string) => {
        if (keybindings.matches(data, "tui.altScreen.lineUp")) body.scrollBy(-1);
        else if (keybindings.matches(data, "tui.altScreen.lineDown")) body.scrollBy(1);
        else if (keybindings.matches(data, "tui.altScreen.pageUp")) body.scrollBy(-12);
        else if (keybindings.matches(data, "tui.altScreen.pageDown")) body.scrollBy(12);
        else if (keybindings.matches(data, "tui.select.cancel") || keybindings.matches(data, "tui.input.submit")) done();
        tui.requestRender();
      },
    };
  }, { overlay: true });
}

// Cover the command shapes seen in the bakery trial, including Make's -C
// option and Python deploy scripts. This remains a heuristic checkpoint:
// Pi's bash tool and arbitrary project scripts are not a security boundary.
const PAID_OR_PUBLISHING_COMMAND =
  /(?:\bep\s+(?:run|survey\s+run|study\s+run|prolific\s+[^\n]*\bpublish|publish)\b|\bmake\b[^\n]*\s(?:data|publish|run|inference)(?:\s|$)|\bpython(?:3)?\b[^\n]*\b(?:deploy|publish|inference)[^\s]*\.py\b)/i;

export default function researchApproval(pi: ExtensionAPI) {
  // Packages installed from Git carry both the shared prompt and Pi adapter.
  // Avoid adding them again if another launcher already supplied the text.
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

  // `ep present` emits a PRESENT_FILE marker for harnesses to handle. Pi has
  // no host artifact pane, so render the local text file in a scrollable TUI
  // overlay when that marker appears in a successful shell result.
  pi.on("tool_result", async (event, ctx) => {
    if (event.toolName !== "bash" || event.isError) return;
    for (const block of event.content) {
      if (block.type !== "text") continue;
      let markerText: string | undefined;
      try {
        const parsed = JSON.parse(block.text);
        markerText = parsed?.data?.presentation_marker;
      } catch {
        // Fall through to the marker scan for output combined with shell text.
      }
      if (typeof markerText !== "string") {
        const marker = block.text.match(/PRESENT_FILE:([^\r\n"]+?)(?:\\t|\t)([^\r\n"]+)/);
        markerText = marker?.[0];
      }
      if (markerText?.startsWith("PRESENT_FILE:")) {
        const [path, title] = markerText.slice("PRESENT_FILE:".length).replace("\\t", "\t").split("\t", 2);
        if (path && title) await showPresentedFile(path, title, ctx);
        return;
      }
    }
  });
}
