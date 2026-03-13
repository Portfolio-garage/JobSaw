---
name: LaTeX_CV_Writing
description: Best practices and strict rules for generating a beautifully styled LaTeX CV using the JobSaw template.
---

# LaTeX CV Writing Guidelines

When generating a CV in LaTeX for the JobSaw project, you must strictly follow these structural and styling rules to ensure the resulting PDF looks professional and compiles without errors.

## 1. Core Principles
*   **Do not alter the preamble.** Keep all `\usepackage`, `\definecolor`, `\hypersetup`, and `\titleformat` commands exactly as they are in the template.
*   **One Page Maximum.** Keep descriptions concise so the entire document fits neatly onto a single A4 page.
*   **Escape Special Characters.** Always escape `&`, `%`, `$`, `#`, `_`, `{`, and `}` by prefixing them with a backslash. Do **not** put backslashes in front of normal words (e.g., do not write `\Google`).

## 2. Header and Contact Information
The header uses the `\begin{center}` environment and `fontawesome5` icons. It should look exactly like this:

```latex
\begin{center}
    {\Huge \textbf{Candidate Name}} \\ \vspace{6pt}
    \small \color{secondary}
    \faMapMarker* City, Country \quad $\cdot$ \quad 
    \faPhone \ +1 234 567 890 \quad $\cdot$ \quad 
    \faEnvelope \ \href{mailto:email@example.com}{email@example.com} \\ \vspace{4pt}
    \href{https://linkedin.com/in/username}{\faLinkedin \ linkedin.com/in/username} \quad $\cdot$ \quad
    \href{https://github.com/username}{\faGithub \ github.com/username} \quad $\cdot$ \quad
    \href{https://portfolio.com}{\faGlobe \ Portfolio Website}
\end{center}
\vspace{6pt}
```
*Rule: Only use `\faMapMarker*`, `\faPhone`, `\faEnvelope`, `\faLinkedin`, `\faGithub`, and `\faGlobe`. Do not invent other FontAwesome commands.*

## 3. Custom Commands
The template defines two custom commands that **MUST** be used for all list entries to maintain consistent alignment and coloring:

### `\resumeEntry{Title}{Date}{Subtitle/Location/Company}{Secondary Subtitle/Location}`
This command takes exactly 4 arguments. Use empty curly braces `{}` if an argument is not needed.

**Example: Education**
```latex
\resumeEntry{B.Sc. in Computer Science}{2020 -- 2024}
{University of Technology}{City, Country}
\begin{itemize}
    \item Coursework: \textbf{Data Structures}, \textbf{Operating Systems}.
\end{itemize}
```

**Example: Experience**
```latex
\resumeEntry{Senior Software Engineer}{Feb 2022 -- Present}
{Tech Corp Inc.}{New York, NY}
\begin{itemize}
    \item Engineered a distributed backend using \textbf{Python} and \textbf{Kafka}, increasing throughput by 40\%.
    \item Migrated legacy services to \textbf{Docker} containers deployed on \textbf{AWS ECS}.
\end{itemize}
```

### `\resumeProject{Project Name}{Technologies Used}`
This command takes exactly 2 arguments and is used for the Projects section.

**Example: Projects**
```latex
\resumeProject{JobSaw -- AI-Driven CV Orchestrator}{Python, LangGraph, Docker}
\begin{itemize}
    \item Architected an autonomous agent pipeline using \textbf{LLMs} for intelligent CV optimization.
\end{itemize}
```

## 4. Section Structure
Sections must start with `\section{Section Name}`. Leave an empty line before and after the section declaration. 

*   **Education:** Use `\resumeEntry`.
*   **Experience:** Use `\resumeEntry`. Follow with an `itemize` block containing 2-3 impact-driven bullets. Bold key technologies (e.g., `\textbf{Python}`).
*   **Projects:** Use `\resumeProject`. Follow with an `itemize` block containing 1-2 impact-driven bullets. Bold key technologies.
*   **Technical Skills:** Do not use `itemize` for skills to save vertical space. Group them categorically using `\noindent` and `\textbf`. Add a `\vspace{2pt}` after the section header.

**Example: Technical Skills**
```latex
\section{Technical Skills}
\vspace{2pt} 

\noindent
\textbf{Core \& Backend:} Python, Java (Spring Boot), C++, Node.js \\
\textbf{Frontend:} React, Vue.js, TypeScript, HTML/CSS \\
\textbf{Data \& Ops:} PostgreSQL, Docker, AWS, Git, Linux
```

## 5. Spacing
*   Use `\vspace{6pt}` or `\vspace{10pt}` sparingly to balance the page if it looks too cramped or too empty.
*   Never use `\\` to create empty lines; trust the template styling (`\titlespacing` and `\setlist`) to handle paragraph separation.
