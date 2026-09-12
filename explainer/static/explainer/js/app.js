const form = document.querySelector("#explainer-form");
const codeInput = document.querySelector("#code-input");
const explainButton = document.querySelector("#explain-button");
const codeCounter = document.querySelector("#code-counter");
const copyButton = document.querySelector("#copy-button");
const profileToggle = document.querySelector("#profile-toggle");
const profileDropdown = document.querySelector("#profile-dropdown");
const themeToggle = document.querySelector("#theme-toggle");
const themeToggleLabel = document.querySelector(".theme-toggle-label");

function setTheme(theme) {
    const isLight = theme === "light";

    document.body.dataset.theme = isLight ? "light" : "dark";

    if (themeToggle) {
        themeToggle.setAttribute("aria-pressed", String(isLight));
    }

    if (themeToggleLabel) {
        themeToggleLabel.textContent = isLight ? "Dark mode" : "Light mode";
    }
}

setTheme(localStorage.getItem("ai-code-explainer-theme") || "dark");

if (themeToggle) {
    themeToggle.addEventListener("click", function () {
        const nextTheme = document.body.dataset.theme === "light" ? "dark" : "light";
        localStorage.setItem("ai-code-explainer-theme", nextTheme);
        setTheme(nextTheme);
    });
}

if (profileToggle && profileDropdown) {
    profileToggle.addEventListener("click", function () {
        const isOpen = profileToggle.getAttribute("aria-expanded") === "true";
        profileToggle.setAttribute("aria-expanded", String(!isOpen));
        profileDropdown.hidden = isOpen;
    });

    document.addEventListener("click", function (event) {
        if (!profileDropdown.contains(event.target) && !profileToggle.contains(event.target)) {
            profileToggle.setAttribute("aria-expanded", "false");
            profileDropdown.hidden = true;
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            profileToggle.setAttribute("aria-expanded", "false");
            profileDropdown.hidden = true;
            profileToggle.focus();
        }
    });
}

function updateCounter() {
    if (!codeInput || !codeCounter) {
        return;
    }

    codeCounter.textContent = `${codeInput.value.length} / 12000`;
}

if (codeInput) {
    codeInput.addEventListener("input", updateCounter);
    updateCounter();

    codeInput.addEventListener("keydown", function (event) {
        if (event.key !== "Tab") {
            return;
        }

        event.preventDefault();

        const value = codeInput.value;
        const start = codeInput.selectionStart;
        const end = codeInput.selectionEnd;

        if (!event.shiftKey) {
            if (start === end) {
                codeInput.value = `${value.slice(0, start)}\t${value.slice(end)}`;
                codeInput.selectionStart = start + 1;
                codeInput.selectionEnd = start + 1;
            } else {
                const lineStart = value.lastIndexOf("\n", start - 1) + 1;
                const lineEndIndex = value.indexOf("\n", end);
                const lineEnd = lineEndIndex === -1 ? value.length : lineEndIndex;
                const selectedLines = value.slice(lineStart, lineEnd);
                const indentedLines = selectedLines
                    .split("\n")
                    .map((line) => `\t${line}`)
                    .join("\n");

                codeInput.value = `${value.slice(0, lineStart)}${indentedLines}${value.slice(lineEnd)}`;
                codeInput.selectionStart = lineStart;
                codeInput.selectionEnd = lineStart + indentedLines.length;
            }
        } else {
            const lineStart = value.lastIndexOf("\n", start - 1) + 1;
            const lineEndIndex = value.indexOf("\n", end);
            const lineEnd = lineEndIndex === -1 ? value.length : lineEndIndex;
            const selectedLines = value.slice(lineStart, lineEnd);
            const unindentedLines = selectedLines
                .split("\n")
                .map((line) => line.replace(/^\t|^ {1,4}/, ""))
                .join("\n");

            codeInput.value = `${value.slice(0, lineStart)}${unindentedLines}${value.slice(lineEnd)}`;
            codeInput.selectionStart = lineStart;
            codeInput.selectionEnd = lineStart + unindentedLines.length;
        }

        updateCounter();
    });
}

if (form) {
    form.addEventListener("submit", function (event) {
        if (!codeInput.value.trim()) {
            event.preventDefault();
            codeInput.focus();
            codeInput.placeholder = "Please paste some code first...";
            return;
        }

        explainButton.disabled = true;
        explainButton.innerHTML = "Explaining... <span>⏳</span>";
    });
}

if (copyButton) {
    copyButton.addEventListener("click", async function () {
        const result = document.querySelector(".result-content");

        if (!result) {
            return;
        }

        await navigator.clipboard.writeText(result.innerText);

        copyButton.textContent = "Copied!";

        setTimeout(function () {
            copyButton.textContent = "Copy explanation";
        }, 1500);
    });
}
