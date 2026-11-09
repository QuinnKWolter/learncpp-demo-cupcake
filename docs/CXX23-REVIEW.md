# C++23 and teaching-quality review

## What changed

The course now has twenty modules with all seven native Cupcake activity schemas: worked example, macro visualization, Parsons puzzle, completion, multiple choice, parameterized tracing, and free coding. Two free-coding integration projects follow modules 14 and 20. This gives 142 activities.

The reviewed authoring sources are `content/modules/*.yaml` and `content/projects.yaml`. Each module contains preparation notes, specific hints for each problem type, explanations for the correct and incorrect choices, a dependency-based puzzle, an authored execution walkthrough, manually stated outputs for all tracing variants, and a purpose for each coding test. `research/editorial-review.json` records the per-module coverage. This is an editorial review record, not evidence of a study with novice learners.

All notes were rewritten, including the advanced modules and both projects. The functions example now announces rectanglePerimeter in a visible geometry.hpp header and defines its calculation below main. The notes explain parameters, argument copies, declarations, definitions, the include guard, call/return, and the separate area task. There is no unexplained pricing.hpp or cost helper.

The recurring activity sequence is: read, inspect an example, step through state changes, arrange blocks, fill a gap, explain a concept, predict a variant, and write a related calculation. This sequence is guidance, not a gate that prevents revisiting an activity.

## Language and toolchain

Every executable activity declares `runtime.language: cpp` and `runtime.version: '23'`. The browser runner explicitly passes `-std=c++23`, `-pedantic-errors`, and `-Werror=return-type`; it does not rely on the compiler's default language version or silently fall back to C++17.

The preexisting system GCC 12.1 compiler was left untouched. A pinned portable WinLibs GCC 16.2 toolchain lives under `.tools/gcc`. Child compiler/program processes receive a PATH containing that toolchain's DLL directory; the user's global PATH is unchanged. Source and digest records are in `research/compiler-provenance.json`. Recreate it with `python tools/setup_compiler.py` when needed.

`tools/verify_cpp23.py` compiles and runs probes for `__cplusplus == 202302L`, `if consteval`, string contains, to_underlying, and expected using the exact execution adapter. The course's string lesson now uses C++23 contains. Familiar constructs such as streams, vectors, and ordinary functions remain appropriate C++23; they were not replaced with unfamiliar new syntax merely for novelty.

References: [GCC standard support](https://gcc.gnu.org/projects/cxx-status.html), [GCC dialect options](https://gcc.gnu.org/onlinedocs/gcc/C_002b_002b-Dialect-Options.html), [pinned WinLibs release](https://github.com/brechtsanders/winlibs_mingw/releases/tag/16.2.0posix-23.1.3-14.0.0-ucrt-r3), and [LearnCpp's C++23 overview](https://www.learncpp.com/cpp-tutorial/introduction-to-c23/).

## Semantic audit

| Area | Review and resulting rule |
| --- | --- |
| Initialization | Whole numbers are initialized before use. Empty braces mean zero for an integer. C++26's changes to uninitialized-value terminology are not presented as C++23 behavior. |
| Arithmetic | Inputs keep signed operations within range. Divisors are positive or explicitly validated. Fractional tasks convert an operand before integer division could discard information. |
| Scope and evaluation order | Static locals persist; their names remain local. Repeated state-changing calls are separate statements, making the intended order explicit. |
| constexpr | Permission to use a function in constant evaluation is distinguished from requiring every call to happen at build time. No C++17-only limitation is used as a C++23 rule. |
| References and returned addresses | Borrowing a reference/pointer does not extend a local object's lifetime. Examples keep referenced objects alive. |
| Range loops and temporaries | All course loops iterate named local containers that remain alive for the whole loop. Their correctness does not depend on either the older temporary-lifetime traps or C++23's range-for lifetime extension. |
| Move and ownership | The empty state after moving a unique_ptr is described specifically for unique_ptr, not asserted for all moved-from types. Objects are not manually double-deleted. |
| Virtual calls | A base reference and a base-value copy are kept distinct. Overrides retain matching const signatures, and polymorphic interfaces have virtual destructors. |
| Parsing | Required fields, numeric range, and trailing data are separate checks. Formatted extraction of a numeric prefix does not establish that the complete record is valid. |
| Incomplete learner functions | Missing returns are compilation errors under the runner's return-type policy, rather than being executed with undefined behavior. |
| Timeout probe | The deliberate nonterminating test uses observable volatile reads; it does not rely on the treatment of a side-effect-free infinite loop, which changes in newer standards. |

This verifies the language mode and the course's actual features/programs. It is not a claim of complete implementation of every C++23 facility in every platform or in the lab's remotely hosted runner.

## Interaction review

- Each activity begins with short control instructions. Topic hints are available before submission, one at a time, without a score penalty.
- Supporting headers are readable above the viewer, and their role is explained in the portable YAML too.
- Code examples in Read & Connect retain line breaks and render as code, rather than being flattened into paragraphs.
- Test examples identify their input, expected output, and reason for being included. Tracing exercises do not reveal their varying output before the learner answers.
- Native codeEdited SPLICE events save free-coding draft regions after the viewer's short debounce. Checked submissions are saved too. Drafts restore by region without replacing the reference source.
- Version 2 uses new activity IDs and its own browser-storage key, preserving the older course's local progress separately.
- Native macro generation is Python-only. These C++ visualizations use manually authored JSVEE actions, C++ source lines, and explained state labels. They are teaching diagrams, not an automatic C++ memory debugger.
- A pinned response-only compatibility patch enables checking unchanged/restored free code. Vendor files remain byte-for-byte intact. The runner still executes the checks; this change never fabricates a passing result.
- Document-level resize messages include expanded help and headers, keeping them from being cut off by the upstream viewer's narrower resize measurement.

## Validation evidence

Run `python tools/validate_course.py`. The report includes all native schemas, reference outputs, every manually expected tracing variant, all twenty visualization outputs, native puzzle answer arrays, allowed interchangeable blocks, rejected wrong dependencies, blank starters, completion distractors, and runtime failure controls. JavaScript and Python syntax checks accompany representative browser journeys. Current results are recorded in `research/validation-results.json` and `research/browser-verification-v2.md`.

`node tools/check_splice_state.mjs` tests the host's real message handler with synthetic messages. `python tools/check_local_service.py` checks the running loopback HTTP integration. Their reports distinguish these checks from browser verification. Computer Use ended on a URL-confidence policy check; revised free-code draft/recheck, trace submission, and Parsons dragging were not signed off end to end in this browser pass. The content review and automated checks are complete; this UI coverage limit remains explicit.
