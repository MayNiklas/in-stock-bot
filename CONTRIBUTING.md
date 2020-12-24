# Contributing to inStockBot

🙏👍🎉 Thanks for taking the time to contribute! 🎉👍🙏

The following is a set of guidelines for contributing to inStockBot. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Table Of Contents

[Code of Conduct](codeOfConduct)

[How Can I Contribute?](#how-can-i-contribute)

* [Suggesting Featurs](#suggesting-features)
* [Reporting Bugs](#reporting-bugs)

[Styleguides](#styleguides)

* [Git Commit Messages](#git-commit-messages)

[Additional Notes](#additional-notes)

* [Issue and Pull Request Labels](#issue-and-pull-request-labels)
  
## Code of Conduct

This project and everyone participating in it is governed by the [Code of Conduct](codeOfConduct). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for inStockBot, including completely new features and minor improvements to existing functionality. Following these guidelines helps maintainers and the community understand your suggestion ✏️ and find related suggestions 💻.

Before creating enhancement suggestions, please check [this list](featureList) as you might find out that you don't need to create one. When you are creating an enhancement suggestion, please [include as many details as possible](#how-do-i-submit-a-good-enhancement-suggestion). Fill in [the template](featureTemplate), including the steps that you imagine you would take if the feature you're requesting existed.

#### How Do I Submit A (Good) Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](issueGuide). After you read the guidelines, create an issue on that repository and provide the following information:

* *Use a clear and descriptive title* for the issue to identify the suggestion.
* *Provide a step-by-step description of the suggested enhancement* in as many details as possible.
* *Provide specific examples to demonstrate the steps*.
* *Describe the current behavior* and *explain which behavior you expected to see instead* and why.
* *Include screenshots and animated GIFs* which help you demonstrate the steps or point out the part of Atom which the suggestion is related to. You can use [this tool](liceCapTool) to record GIFs on macOS and Windows, and [this tool](silentCastTool) or [this tool](byzanzTool) on Linux.
* *Specify the name and version of the OS you're using.*

### Reporting Bugs

This section guides you through submitting a bug report for inStockBot. Following these guidelines helps maintainers and the community understand your report ✏️, reproduce the behavior 💻, and find related reports.

Before creating bug reports, please check [this list](issueList) as you might find out that you don't need to create one. When you are creating a bug report, please [include as many details as possible](#how-do-i-submit-a-good-bug-report). Fill out [the required template](issueReport), the information it asks for helps us resolve issues faster.

> *Note:* If you find a *Closed* issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

#### How Do I Submit A (Good) Bug Report?

Bugs are tracked as [GitHub issues](issueGuide). Create an issue and provide the following information by filling in [the template](issueTemplate).

Explain the problem and include additional details to help maintainers reproduce the problem:

* *Use a clear and descriptive title* for the issue to identify the problem.
* *Describe the exact steps which reproduce the problem* in as many details as possible. For example, start by explaining how you started Atom, e.g. which command exactly you used in the terminal, or how you started Atom otherwise. When listing steps, *don't just say what you did, but explain how you did it*. For example, if you moved the cursor to the end of a line, explain if you used the mouse, or a keyboard shortcut or an Atom command, and if so which one?
* *Provide specific examples to demonstrate the steps*. Include links to files or GitHub projects, or copy/pasteable snippets, which you use in those examples. If you're providing snippets in the issue, use [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* *Describe the behavior you observed after following the steps* and point out what exactly is the problem with that behavior.
* *Explain which behavior you expected to see instead and why.*
* *Include screenshots and animated GIFs* which show you following the described steps and clearly demonstrate the problem. If you use the keyboard while following the steps, *record the GIF with the [Keybinding Resolver](keybindingTool) shown*. You can use [this tool](liceCapTool) to record GIFs on macOS and Windows, and [this tool](silentCastTool) or [this tool](byzanzTool) on Linux.
* **If the problem wasn't triggered by a specific action**, describe what you were doing before the problem happened and share more information using the guidelines below.

Provide more context by answering these questions:

* *Did the problem start happening recently* (e.g. after updating to a new version) or was this always a problem?
* If the problem started happening recently, *can you reproduce the problem in an older version?*
* *Can you reliably reproduce the issue?* If not, provide details about how often the problem happens and under which conditions it normally happens.
* If the problem is related to working with files (e.g. opening and editing files), *does the problem happen for all files and projects or only some?* Does the problem happen only when working with local or remote files (e.g. on network drives), with files of a specific type (e.g. only Python oder Docker files), with large files or files with very long lines, or with files in a specific encoding? Is there anything else special about the files you are using?

Include details about your configuration and environment:

* *Which version are you using?* You can get the exact version by running `python -v` in your terminal, or by `docker -v`
* *What's the name and version of the OS you're using*?

### Pull Requests

The process described here has several goals:

* Fix problems that are important to users

Please follow these steps to have your contribution considered by the maintainers:

1. Follow all instructions in [the template](featureTemplate)
2. Follow the [styleguides](#styleguides)
3. After you submit your pull request, verify that all [status checks](statusCheck) are passing <details><summary>What if the status checks are failing?</summary>If a status check is failing, and you believe that the failure is unrelated to your change, please leave a comment on the pull request explaining why you believe the failure is unrelated. A maintainer will re-run the status check for you. If we conclude that the failure was a false positive, then we will open an issue to track that problem with our status check suite.</details>

While the prerequisites above must be satisfied prior to having your pull request reviewed, the reviewer(s) may ask you to complete additional design work, tests, or other changes before your pull request can be ultimately accepted.

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* When only changing documentation, include `[ci skip]` in the commit title
* Consider starting the commit message with an applicable emoji:
  * 🎨 `:art:` when improving the format/structure of the code
  * 🐎 `:racehorse:` when improving performance
  * 🚰 `:non-potable_water:` when plugging memory leaks
  * 📝 `:memo:` when writing docs
  * 🐧 `:penguin:` when fixing something on Linux
  * 🍏 `:apple:` when fixing something on macOS
  * 🪟 `:checkered_flag:` when fixing something on Windows
  * 🐛 `:bug:` when fixing a bug
  * 🔥 `:fire:` when removing code or files
  * 💚 `:green_heart:` when fixing the CI build
  * 🏴󠁤󠁭󠀰󠀸󠁿 `:white_check_mark:` when adding tests
  * 🔒 `:lock:` when dealing with security
  * ⬆️ `:arrow_up:` when upgrading dependencies
  * ⬇️ `:arrow_down:` when downgrading dependencies
  * 👕 `:shirt:` when removing linter warnings

### Documentation Styleguide

* // TODO

#### Example

```python
// TODO
```

## Additional Notes

### Issue and Pull Request Labels

This section lists the labels we use to help us track and manage issues and pull requests. Most labels are used across all repositories.

[GitHub search](searchGuide) makes it easy to use labels for finding groups of issues or pull requests you're interested in.

#### Type of Issue and Issue State

| Label name | Description |
| --- | --- |
| `bug` | Confirmed bugs or reports that are very likely to be bugs. |
| `documentation` | Create new or update documentation. |
| `duplicate` | Issues which are duplicates of other issues, i.e. they have been reported before. |
| `enhancement` | Feature requests. |
| `good first issue` | Less complex issues which would be good first issues to work on for users who want to contribute to inStockBot. |
| `help-wanted` | The Atom core team would appreciate help from the community in resolving these issues. |
| `invalid` | Not a Issue. |
| `question` | Questions more than bug reports or feature requests (e.g. how do I do X). |
| `wontfix` | The Atom core team has decided not to fix these issues for now, either because they're working as intended or for some other reason. |

#### Pull Request Labels

| Label name  | Description
| --- | --- |
| `work-in-progress` | Pull requests which are still being worked on, more changes will follow. |
| `needs-review` | Pull requests which need code review, and approval from maintainers or Atom core team. |
| `under-review` | Pull requests being reviewed by maintainers or Atom core team. |
| `requires-changes` | Pull requests which need to be updated based on review comments and then reviewed again. |
| `needs-testing` | Pull requests which need manual testing. |

[codeOfConduct]: https://github.com/MayNiklas/in-stock-bot/blob/main/CODE_OF_CONDUCT.md
[featureList]: https://github.com/MayNiklas/in-stock-bot/labels/enhancement
[featureTemplate]: https://github.com/MayNiklas/in-stock-bot/blob/main/.github/ISSUE_TEMPLATE/feature-request.md
[issueList]: https://github.com/MayNiklas/in-stock-bot/issues
[issueTemplate]: https://github.com/MayNiklas/in-stock-bot/blob/main/.github/ISSUE_TEMPLATE/issue-template.md
[issueGuide]: https://guides.github.com/features/issues/
[searchGuide]: https://help.github.com/articles/searching-issues/
[statusCheck]: https://help.github.com/articles/about-status-checks/
[liceCapTool]: https://www.cockos.com/licecap
[silentCastTool]: https://github.com/colinkeenan/silentcast
[byzanzTool]: https://github.com/GNOME/byzanz
[keybindingTool]: https://github.com/atom/keybinding-resolver
