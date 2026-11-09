# C++23 practice with Cupcake

20 prepared modules, each with all seven native activity types, plus two integration projects.

## 01. Your first C++ programs

### Start with a small program
A program is a list of instructions for the computer. C++ begins running your instructions inside `main`. The braces `{` and `}` surround the instructions that belong to it. A semicolon `;` ends a statement. `#include <iostream>` makes the standard input and output tools available; you do not need to write those tools yourself.

An `int` stores a whole number. `int boxes{4};` creates a variable named `boxes` and gives it the starting value 4. Empty braces, as in `int n{};`, give an integer the value zero. In this course we always give local numbers a starting value before using them.

### Read a calculation, one line at a time
`*` multiplies two numbers. With four boxes and three items in each, `boxes * perBox` counts the items altogether. The result is stored in `total`; the two starting values stay the same.

```cpp
int boxes{4};
int perBox{3};
int total{boxes * perBox};
std::cout << total << '\n';
```

`std::cout` is the output stream: each `<<` sends the next value to it. The `std::` part says that this tool comes from the standard library. `'\n'` means “start a new line.” It is not part of the number being printed. The example prints one number on its own line.

### When the starting value comes from input
`std::cin >> n;` reads a whole number into `n`. The Write code activity already includes that line. Your job is to calculate the square: a number multiplied by itself. For example, the square of 3 is 9; the square of −3 is also 9. You do not need a power function or a loop.

### Your route through the activities
- Read the annotations in Worked example; Step through shows how the values change.
- Arrange code and Fill gaps focus on the box calculation. Use “items altogether” to choose the operation.
- Explain why asks about empty braces. Predict output changes the number of boxes; use the number shown in your program.
- Write code asks for a square instead. Only the marked line is yours to edit; the other lines read the input and start/end the program.

### Check your reasoning
A compiler translates source code into a runnable program and checks its syntax. A successful build does not guarantee the calculation is right. Use a positive number, zero, and a negative number to check your square. Read a compiler error from its first line; one missing semicolon can cause several later messages.

- [Build a program](https://www.learncpp.com/cpp-tutorial/introduction-to-cpp-development/)
- [Initialization](https://www.learncpp.com/cpp-tutorial/variable-assignment-and-initialization/)

- [Worked example](activities/01-first-programs/worked-example.yaml)
- [Step through](activities/01-first-programs/macro-visualization.yaml)
- [Arrange code](activities/01-first-programs/parsons-puzzles.yaml)
- [Fill gaps](activities/01-first-programs/code-completion.yaml)
- [Explain why](activities/01-first-programs/multiple-choice-question.yaml)
- [Predict output](activities/01-first-programs/parameterized-code-tracing.yaml)
- [Write code](activities/01-first-programs/free-coding.yaml)

## 02. Functions, declarations, and files

### A function is a named calculation
A function lets us give a useful calculation a name and call it when we need it. In this module we calculate a rectangle's perimeter: the distance around its four sides. The rule is `2 * (width + height)` because there are two widths and two heights.

```cpp
int rectanglePerimeter(int width, int height) {
    return 2 * (width + height);
}
```

The first `int` says the function gives back a whole number. `width` and `height` are parameters: names for the values supplied by a call. In `rectanglePerimeter(3, 5)`, 3 becomes width and 5 becomes height for that call. The parentheses in the calculation add the dimensions before multiplying. `return` sends the answer back to the calling line and ends that call. It does not print anything. `std::cout` prints the returned answer in `main`.

### Why are there two files?
The example deliberately separates the function's announcement from its instructions. A **declaration** announces the name, result type, and parameter types. A **definition** also supplies the body in braces. The compiler needs an announcement before the first call.

The supplied `geometry.hpp` header contains this declaration:

```cpp
int rectanglePerimeter(int width, int height);
```

`#include "geometry.hpp"` makes that announcement available to `main.cpp`. The double quotes mean this is a file supplied with the exercise. Open **Supporting file: geometry.hpp** above the activity to read it. Its `#ifndef`, `#define`, and `#endif` lines are an include guard: they keep this header's contents from being included twice in one source file. You do not need to edit the guard.

The complete function definition is visible below `main` in the program. Read its body to see the whole calculation, then follow the returned number back to main. Both files are supplied when you check an answer.

### Follow a call and come back
For width 3 and height 5, enter the function, calculate `2 * (3 + 5)`, and return to the output line. The parameters belong to this call; another call can use different dimensions. This same call-and-return sequence is shown in Step through and Predict output.

### Use the idea in a new task
Write code asks for **area**, the number of unit squares inside a rectangle, rather than perimeter. Area is `width * height`. The function name, parameters, input, and output lines are supplied. Write only the return calculation. Check a rectangle and a square: the same formula must work for both. Never print from the function just to display the answer; the supplied `main` already does that.

- [Function parameters](https://www.learncpp.com/cpp-tutorial/introduction-to-function-parameters-and-arguments/)
- [Header files](https://www.learncpp.com/cpp-tutorial/header-files/)

- [Worked example](activities/02-functions-files/worked-example.yaml)
- [Step through](activities/02-functions-files/macro-visualization.yaml)
- [Arrange code](activities/02-functions-files/parsons-puzzles.yaml)
- [Fill gaps](activities/02-functions-files/code-completion.yaml)
- [Explain why](activities/02-functions-files/multiple-choice-question.yaml)
- [Predict output](activities/02-functions-files/parameterized-code-tracing.yaml)
- [Write code](activities/02-functions-files/free-coding.yaml)

## 03. Debug by tracing, then testing

### When a program runs but gives the wrong answer
A compiler catches many spelling and structure mistakes. A program can still build and do the wrong calculation. To debug means to find why the actual behavior differs from what we intended. Start with a small example and say what the result should be before changing code.

This module swaps two values. If left starts at 2 and right starts at 9, the intended final pair is 9 and 2. Read assignment as “calculate the right side now, then store it in the name on the left.” An assignment does not preserve the old value for later.

### Keep a value before replacing it
```cpp
int saved{left};
left = right;
right = saved;
```

First, saved keeps the original left value. Next, left receives right's value. Finally, right receives the saved original value. In `left = right; right = left;`, the second line sees the already changed left, so both variables end up with the same value. The temporary variable is there to prevent that loss.

### How to trace the example
Make three columns headed left, right, and saved. After each line, change only the value that line assigns. Step through makes that little table visible. Predict output changes a starting value, so always begin with the values on your own screen.

Arrange code and Fill gaps ask you to preserve the old value before it is overwritten. Explain why asks which input would expose a faulty swap. Two equal numbers are a weak test: even broken code can appear to swap them correctly. Two different numbers make the error visible.

### Your coding task
The supplied input lines read a and b; the output line prints them after your marked block. Use a third variable to preserve the original a before replacing it. Try unequal inputs, equal inputs, and a negative input. A failed case is a clue about your reasoning, not a reason to make a special rule for that one input.

In a desktop debugger, a breakpoint pauses a program and stepping runs one instruction at a time. You can use that tool later. Here the table, highlighted lines, and test results support the same habit: find the first line where a value stops matching your prediction.

- [Debugging strategy](https://www.learncpp.com/cpp-tutorial/a-strategy-for-debugging/)
- [Watching values](https://www.learncpp.com/cpp-tutorial/using-an-integrated-debugger-watching-variables/)

- [Worked example](activities/03-debugging/worked-example.yaml)
- [Step through](activities/03-debugging/macro-visualization.yaml)
- [Arrange code](activities/03-debugging/parsons-puzzles.yaml)
- [Fill gaps](activities/03-debugging/code-completion.yaml)
- [Explain why](activities/03-debugging/multiple-choice-question.yaml)
- [Predict output](activities/03-debugging/parameterized-code-tracing.yaml)
- [Write code](activities/03-debugging/free-coding.yaml)

## 04. Choose the right arithmetic type

### Whole numbers and fractional numbers
An `int` is useful for counts such as a number of students. A `double` can represent a fractional measurement such as an average. The types of the numbers being divided determine how division happens.

With two integers, `/` performs whole-number division. For positive 15 and 4, the result is 3: the fractional part is discarded. Giving that already computed result to a double afterward produces 3.0, not 3.75.

### Convert before the division
```cpp
double average{static_cast<double>(sum) / count};
```

`static_cast<double>(sum)` means “use a double version of sum in this expression.” It does not change sum itself. Now one operand is a double, so the division can produce a fractional result. The example prints the integer division and the fractional division side by side so you can compare them.

Step through and Predict output use a small quotient. Arrange code asks you to put the inputs before the calculation and the calculation before its output. Fill gaps asks where the conversion belongs. Explain why checks a common misunderstanding: a double on the left does not travel backward and change an integer calculation on the right.

### Your coding task: an average of two scores
Add the two input scores and divide by two. Convert before dividing so an odd total can produce a half point. The surrounding output code is supplied: `std::fixed` together with `std::setprecision(1)` asks for exactly one digit after the decimal point, such as 7.5 or 0.0. `<iomanip>` provides the precision setting. You do not need to change these display settings.

### Useful limits
Floating-point numbers store approximations; many decimal fractions are not exact internally. We compare the formatted text requested by the task. Counts and scores are kept small so the integer sums fit safely. Dividing by zero is invalid, and the examples always use a positive count. Later modules discuss detecting invalid input rather than assuming it is valid.

- [Integers](https://www.learncpp.com/cpp-tutorial/signed-integers/)
- [Floating point](https://www.learncpp.com/cpp-tutorial/floating-point-numbers/)

- [Worked example](activities/04-types/worked-example.yaml)
- [Step through](activities/04-types/macro-visualization.yaml)
- [Arrange code](activities/04-types/parsons-puzzles.yaml)
- [Fill gaps](activities/04-types/code-completion.yaml)
- [Explain why](activities/04-types/multiple-choice-question.yaml)
- [Predict output](activities/04-types/parameterized-code-tracing.yaml)
- [Write code](activities/04-types/free-coding.yaml)

## 05. Constants and text with clear lifetimes

### Keep text in a string
`std::string` stores text and owns its characters. Add `<string>` when using it. A string can contain spaces; `.size()` reports how many characters are stored. We use ASCII input in these activities so “characters” has the simple meaning you expect.

`const` means the object cannot be changed after its initial value is supplied. The example's word stays fixed while we ask a question about it.

### A C++23 question about text
```cpp
const std::string word{"cupcake"};
std::cout << std::boolalpha << word.contains("cake") << '\n';
```

`.contains("cake")` asks whether that sequence of letters appears anywhere in word. It returns a `bool`, a true/false value. `std::boolalpha` tells the output stream to display the words true and false rather than 1 and 0. `contains` became a standard string operation in C++23. It differs from `starts_with`, which only checks the beginning, and `empty`, which asks whether the string has zero characters.

### Read a whole line
For the Write code task, `std::getline(std::cin, text)` reads a whole line, including spaces, into text. It does not store the ending newline. The input code has no earlier numeric read, so there is no leftover newline to handle. Call `.size()` on the resulting string and print that number. An empty input line is valid and has length zero.

### Owning text and viewing text
Explain why compares a string with `std::string_view`. A view is a way to look at characters stored somewhere else; it does not keep its own copy. If that other storage disappears, the view cannot safely be used. Imagine borrowing a book: the borrowing slip does not create a second book. The examples keep their text alive for every use; you do not need to construct a dangling view.

The walkthrough follows the contains question. The puzzle builds a small text question, and Predict output changes text before checking its length. In every activity, check whether the operation asks about length, contents, or ownership—these are different questions.

- [Constants](https://www.learncpp.com/cpp-tutorial/constant-variables-named-constants/)
- [Strings](https://www.learncpp.com/cpp-tutorial/introduction-to-stdstring/)
- [String views](https://www.learncpp.com/cpp-tutorial/introduction-to-stdstring_view/)

- [Worked example](activities/05-constants-strings/worked-example.yaml)
- [Step through](activities/05-constants-strings/macro-visualization.yaml)
- [Arrange code](activities/05-constants-strings/parsons-puzzles.yaml)
- [Fill gaps](activities/05-constants-strings/code-completion.yaml)
- [Explain why](activities/05-constants-strings/multiple-choice-question.yaml)
- [Predict output](activities/05-constants-strings/parameterized-code-tracing.yaml)
- [Write code](activities/05-constants-strings/free-coding.yaml)

## 06. Operators, conditions, and bit flags

### Build a decision from small questions
A comparison gives a true/false answer. `age >= 12` asks whether age is at least twelve; `age <= 17` asks whether it is at most seventeen. `>=` and `<=` include the endpoint. `>` and `<` do not.

```cpp
bool eligible{age >= 12 && age <= 17};
```

`bool` stores true or false. `&&` means **both conditions must be true**. In the example, an eligible age must meet both bounds. `||` means **at least one condition is true**. Substituting OR here would be a mistake: every age is either at least twelve or at most seventeen, even an age outside the intended group. `std::boolalpha` prints the result as the words true and false.

### Give each comparison its own value
In mathematics you may write a chained inequality. In C++, write `0 <= n && n <= 10`. `0 <= n <= 10` first works out `0 <= n` and then compares that true/false result with 10. It no longer checks both bounds of n. Explain why asks you to recognize this change in meaning.

### Ask whether a number is even
`n % 2` gives the remainder after dividing by two. For an even integer that remainder is zero, so `n % 2 == 0` asks “is n even?” `==` compares values; a single `=` assigns a value. These are different operations.

The coding task combines three questions: at least 10, at most 20, and even. All three must hold, so join them with AND. The supplied input and output lines are ready; write the condition in the marked declaration. Check both endpoints, an odd number inside, and an even number outside.

### Why order can matter
Logical AND and OR can stop early once the answer is known. This is called short-circuiting. No later check can make a failed AND true. The optional bit-flags reading describes `&` and `|`, which work on individual bits and are not substitutes for `&&` and `||`. You do not need bit manipulation for these activities.

Step through checks the two age bounds separately. Predict output changes an age, while the puzzle helps connect a comparison, a Boolean result, and its printed display.

- [Arithmetic](https://www.learncpp.com/cpp-tutorial/arithmetic-operators/)
- [Logic](https://www.learncpp.com/cpp-tutorial/logical-operators/)
- [Bit flags](https://www.learncpp.com/cpp-tutorial/bit-flags-and-bit-manipulation-via-stdbitset/)

- [Worked example](activities/06-operators/worked-example.yaml)
- [Step through](activities/06-operators/macro-visualization.yaml)
- [Arrange code](activities/06-operators/parsons-puzzles.yaml)
- [Fill gaps](activities/06-operators/code-completion.yaml)
- [Explain why](activities/06-operators/multiple-choice-question.yaml)
- [Predict output](activities/06-operators/parameterized-code-tracing.yaml)
- [Write code](activities/06-operators/free-coding.yaml)

## 07. Scope, duration, and linkage

### Where a name can be used, and how long a value stays
**Scope** describes where a name is available in the source. A variable declared inside a function can normally be named only inside that function's block. **Lifetime** describes how long its stored object exists. These are related questions, but they are not the same question.

An ordinary local integer is created again on each call. A `static` local integer keeps its value between calls:

```cpp
int nextTicket() {
    static int ticket{0};
    return ++ticket;
}
```

The starting zero is supplied once. `++ticket` means “increase ticket by one, then use the increased value.” The first call returns one; the next call begins with the value left by the previous call. The name ticket is still local to this function: static does not make it a global name. The two calls in the example are deliberately separate statements so their order is easy to follow.

### Put related functions under a clear name
A **namespace** groups names. The supplied coding task defines `toMinutes` inside `namespace units`. Its caller writes `units::toMinutes(hours)`: the `::` says “look for toMinutes inside units.” A namespace is an organization tool; it does not change the hours-to-minutes calculation.

```cpp
namespace units {
    int toMinutes(int hours) {
        // Your calculation goes here.
    }
}
```

An hour contains sixty minutes. Return that conversion using the existing parameter; `main` reads the input and prints the result. No extra header or hidden helper is required.

### Keep the ideas separate while practicing
The example, visualization, puzzle, and prediction concern the remembered ticket value. Explain why asks whether a local name can have a long-lived value. Write code applies namespace organization to a different function. If a result surprises you, first ask “which declaration does this name refer to?” and then “is this a new object or a value kept from an earlier call?”

The wider LearnCpp chapter also discusses linkage, the rules for connecting names across source files, and shadowing, where an inner name hides an outer one. Those are follow-up reading topics; no exercise here depends on an unexplained multi-file linkage rule.

- [Namespaces](https://www.learncpp.com/cpp-tutorial/user-defined-namespaces-and-the-scope-resolution-operator/)
- [Static locals](https://www.learncpp.com/cpp-tutorial/static-local-variables/)

- [Worked example](activities/07-scope/worked-example.yaml)
- [Step through](activities/07-scope/macro-visualization.yaml)
- [Arrange code](activities/07-scope/parsons-puzzles.yaml)
- [Fill gaps](activities/07-scope/code-completion.yaml)
- [Explain why](activities/07-scope/multiple-choice-question.yaml)
- [Predict output](activities/07-scope/parameterized-code-tracing.yaml)
- [Write code](activities/07-scope/free-coding.yaml)

## 08. Branches and loops

### Repeat a small step with a loop
A loop lets a program repeat instructions. A counting `for` loop has three parts in its parentheses: a starting step, a question checked before each repetition, and an update performed after each repetition.

```cpp
for (int i{1}; i <= limit; ++i) {
    total += i;
}
```

Start i at 1. If i is no larger than limit, run the body. `total += i` means the same as `total = total + i`. Next, `++i` increases i by one. Check the condition again. When the condition is false, continue after the loop.

### A running total starts before the loop
The example sets `total` to zero before adding anything. A value that collects contributions is often called an accumulator. If you set it to zero inside the loop, earlier contributions would be lost. For limit 3, the totals after the three visits are 1, 3, and 6. Step through shows each visit separately.

`<=` includes the limit; `<` leaves it out. For an empty range the body need not run at all. Predict output varies the limit, so test the condition before assuming there will be a first repetition. Explain why uses a loop starting at zero: count the values that pass its condition, not just the endpoint printed in the source.

### Your new sequence: positive even numbers
Write code adds 2, 4, 6, and so on, stopping when the next number is greater than n. You can start at 2 and update by two (`value += 2`). Keep the total outside the loop and print once after it finishes. If n is zero or one, there are no positive even numbers to add, so the answer is zero.

Arrange code focuses on the same ordering: initialize the total, add the contributions, then display the finished answer. The wider reading also introduces `if` for choosing a path and `switch` for choosing a named case. Neither is required for this particular even-number loop.

- [For loops](https://www.learncpp.com/cpp-tutorial/for-statements/)
- [Switch](https://www.learncpp.com/cpp-tutorial/switch-statement-basics/)

- [Worked example](activities/08-control-flow/worked-example.yaml)
- [Step through](activities/08-control-flow/macro-visualization.yaml)
- [Arrange code](activities/08-control-flow/parsons-puzzles.yaml)
- [Fill gaps](activities/08-control-flow/code-completion.yaml)
- [Explain why](activities/08-control-flow/multiple-choice-question.yaml)
- [Predict output](activities/08-control-flow/parameterized-code-tracing.yaml)
- [Write code](activities/08-control-flow/free-coding.yaml)

## 09. Input validation and meaningful tests

### Parsing a value is not the same as accepting it
Input has two questions: “can I read an integer?” and “is that integer allowed?” The word oops fails the first question. The number 101 can be read as an integer but is outside the allowed score range. Both deserve a clear response.

```cpp
if (!(std::cin >> score)) {
    std::cout << "invalid\n";
    return 0;
}
```

`if` runs its block only when the condition is true. Here the read can report failure; `!` reverses that result so the error block runs when reading fails. `return 0;` in main stops this run normally after printing its message. It avoids using the initial zero as though the user had entered a valid score.

After a successful read, the example checks that the score is between 0 and 100, including both endpoints. An `else` block provides the alternative action when an if condition is false.

### Divide valid scores into two groups
The coding task prints pass for 60 through 100 and retry for 0 through 59. It prints invalid for malformed input or an out-of-range integer. Check reading and range first. Then, among valid scores, compare with the pass threshold. `else if` tests the next condition only when the earlier one did not choose a block.

The supplied tests each have a job: 60 tests the first passing score; 59 tests the neighboring retry score; zero and 100 test the valid endpoints; text and out-of-range values test rejection. A good repair follows one general rule for all of them.

### What an assertion is for
An assertion (`assert`) checks a programmer's assumption, such as “this internal count should never be negative.” It can be disabled in a release build. It is not a reliable way to tell a user that their input is unacceptable. Explain why asks about this distinction; the coding task uses ordinary if/else handling instead.

Step through follows one valid score, and Predict output varies that score. The puzzle puts validation before success output. None of these tasks asks you to keep retrying after a failed read: report the required result once and finish.

- [Testing](https://www.learncpp.com/cpp-tutorial/introduction-to-testing-your-code/)
- [Invalid input](https://www.learncpp.com/cpp-tutorial/stdcin-and-handling-invalid-input/)

- [Worked example](activities/09-validation/worked-example.yaml)
- [Step through](activities/09-validation/macro-visualization.yaml)
- [Arrange code](activities/09-validation/parsons-puzzles.yaml)
- [Fill gaps](activities/09-validation/code-completion.yaml)
- [Explain why](activities/09-validation/multiple-choice-question.yaml)
- [Predict output](activities/09-validation/parameterized-code-tracing.yaml)
- [Write code](activities/09-validation/free-coding.yaml)

## 10. Conversions and type deduction

### auto follows the initializer you actually wrote
`auto` asks the compiler to work out a variable's type from its starting expression. It does not mean that the variable can later change type. In `auto count{6};`, 6 is an integer literal, so count is an int.

```cpp
auto whole{9 / 2};
auto fraction{static_cast<double>(9) / 2};
```

In the first line, both operands are integers. Division drops the fraction and produces an int result. In the second line, the explicit conversion supplies a double before division, so the result and the deduced variable type are double. `auto` accepts those results; it does not correct an earlier calculation for us.

### Place the conversion where the information would be lost
`static_cast<double>(9 / 2)` converts a quotient that has already lost its fractional part. `static_cast<double>(9) / 2` instead lets the division keep a fractional result. Fill gaps asks you to choose between these points in the calculation. Step through and Predict output keep the two results side by side.

### Your coding task: total divided by count
The supplied code reads total and count as integers. Count is guaranteed to be positive. Create average from a fractional division and leave the supplied output line in place. `<iomanip>`, `std::fixed`, and `std::setprecision(2)` make the display use exactly two digits after the decimal point, such as 4.50. The formatting is provided so you can focus on the calculation.

### A helpful compiler check
Braces reject many conversions that could lose information, called narrowing conversions. For example, `int n{2.5};` is rejected rather than quietly throwing away the half. A type alias gives an existing type another name; it does not create a new kind of numeric storage. These wider chapter ideas explain why clear type choices matter, but no activity requires an unfamiliar alias.

When checking an answer, ask what type each operand has **before** the operation. Then ask what type its result has. Do those in that order, before thinking about the destination variable's name.

- [Explicit casts](https://www.learncpp.com/cpp-tutorial/explicit-type-conversion-casting-and-static-cast/)
- [auto](https://www.learncpp.com/cpp-tutorial/type-deduction-for-objects-using-the-auto-keyword/)

- [Worked example](activities/10-conversions/worked-example.yaml)
- [Step through](activities/10-conversions/macro-visualization.yaml)
- [Arrange code](activities/10-conversions/parsons-puzzles.yaml)
- [Fill gaps](activities/10-conversions/code-completion.yaml)
- [Explain why](activities/10-conversions/multiple-choice-question.yaml)
- [Predict output](activities/10-conversions/parameterized-code-tracing.yaml)
- [Write code](activities/10-conversions/free-coding.yaml)

## 11. Overloads, templates, and constexpr

### One calculation, more than one numeric type
Suppose we want the larger of two values. We could write one function for integers and another for doubles. Functions can share a name when their parameter lists differ; these are overloads. A **function template** lets us write one pattern for both cases instead.

```cpp
template <typename T>
constexpr T larger(T a, T b) {
    return a < b ? b : a;
}
```

Read T as “the type chosen for this call.” For `larger(3, 8)`, the compiler uses int. For `larger(2.5, 1.5)`, it uses double. Both arguments in these activities have the same type, so there is no ambiguous mixed-type call to resolve.

### Read the choice expression
The conditional expression `condition ? whenTrue : whenFalse` chooses one of two values. Here, if a is less than b, return b; otherwise return a. Only one result is returned. This is a shorter way to write an if/else decision, not a new arithmetic operation.

### What constexpr promises
A `constexpr` variable needs a value available while the program is being built. A `constexpr` function is allowed to calculate such a value when its inputs and use permit it. It can also run later with values read during execution. The example uses a compile-time call for best; the coding task uses runtime input. Explain why asks why those uses are both possible. C++23 has additional compile-time tools, but they do not change this distinction.

### Transfer the idea to a smaller-value function
Write code supplies the template header and asks you to return the smaller of a and b. Keep the return type T and return one of the original values, rather than converting everything to int. The caller tests an integer pair and a fixed double pair, so a solution that quietly drops fractions will be exposed.

Step through and Predict output follow a single larger-value call. Arrange code orders preparation, a call, and its output. When reasoning about any template here, first name the chosen type, then apply the ordinary comparison rule you already know.

- [Function templates](https://www.learncpp.com/cpp-tutorial/function-templates/)
- [Constexpr functions](https://www.learncpp.com/cpp-tutorial/constexpr-functions/)

- [Worked example](activities/11-generic-functions/worked-example.yaml)
- [Step through](activities/11-generic-functions/macro-visualization.yaml)
- [Arrange code](activities/11-generic-functions/parsons-puzzles.yaml)
- [Fill gaps](activities/11-generic-functions/code-completion.yaml)
- [Explain why](activities/11-generic-functions/multiple-choice-question.yaml)
- [Predict output](activities/11-generic-functions/parameterized-code-tracing.yaml)
- [Write code](activities/11-generic-functions/free-coding.yaml)

## 12. References, pointers, and optional results

### Two names can refer to one value
An ordinary int parameter receives its own copy of an argument. An `int&` parameter instead refers to the caller's existing integer. This is a **reference**: another way to name the same object. In `addBonus(int& score)`, changing score changes the integer supplied by the caller. `void` means the function performs an action without returning a separate result value.

```cpp
void addBonus(int& score) {
    score += 5;
}
```

Do not draw a second independent score in your trace table. The caller and this parameter refer to one integer. A `const int&` permits reading through that reference but not changing the integer through it.

### A pointer stores where an object is
`int* pointer{&score};` stores the address of score. Here `&score` means “the address of score,” whereas the & in the parameter declaration means a reference type. `*pointer` accesses the integer at that stored address. A pointer can be `nullptr`, meaning it does not point at an object; check before using `*pointer` when null is possible.

The example's pointer refers to the same score that addBonus changed. It does not create another score, and it does not take responsibility for keeping that object alive.

### A name cannot keep a destroyed object alive
A local automatic integer normally exists only until its function call ends. Returning its address would leave the caller with a pointer to an object whose lifetime is over. Returning a reference has the same problem. Explain why asks about this lifetime issue, not whether an address can be copied.

The wider reading introduces `std::optional<T>` for a result that may be absent: check whether it contains a value before reading it. It is an alternative result design, not a requirement in these exercises.

### Your action: replace negative values with zero
Write code supplies `clampToZero(int& value)`. If value is negative, assign zero; otherwise leave it alone. Do not add an output statement or return a number: main prints the caller's integer after your action. Step through, Arrange code, and Predict output make the effect of an alias visible so you can connect a changed parameter with a changed caller.

- [References](https://www.learncpp.com/cpp-tutorial/lvalue-references/)
- [Pointers](https://www.learncpp.com/cpp-tutorial/introduction-to-pointers/)
- [Optional](https://www.learncpp.com/cpp-tutorial/stdoptional/)

- [Worked example](activities/12-references/worked-example.yaml)
- [Step through](activities/12-references/macro-visualization.yaml)
- [Arrange code](activities/12-references/parsons-puzzles.yaml)
- [Fill gaps](activities/12-references/code-completion.yaml)
- [Explain why](activities/12-references/multiple-choice-question.yaml)
- [Predict output](activities/12-references/parameterized-code-tracing.yaml)
- [Write code](activities/12-references/free-coding.yaml)

## 13. Enums, structs, and aggregate values

### Keep related facts together
A **struct** groups named pieces of information into one record. The example's Parcel has a weight and a status. `int weight{};` gives weight a zero default. `Status status{Status::waiting};` gives status a waiting default. A semicolon also follows the closing brace of a struct definition.

`Parcel parcel{4, Status::ready};` supplies values in member declaration order: first weight, then status. The dot in `parcel.weight` selects a named member of that object. This avoids confusing two unrelated numbers just because they happen to be next to each other.

### Name a choice with an enum class
```cpp
enum class Status { waiting, ready };
```

This defines two named Status values. `Status::ready` means “the ready value from Status.” The `::` is the same scope separator used for namespaces earlier. `Status.ready` would instead try to select a member of an object; Status is a type, not an object. Enumerators are values, so no function-call parentheses are needed.

The example initializes a ready parcel and prints its weight only when its status matches that named value. The visualization and prediction show the choice; the code puzzle orders record construction, a decision, and output.

### Make a new record without changing the old one
The coding task supplies `struct Point { int x{}; int y{}; };`. A point's x is its horizontal coordinate and y is its vertical coordinate. `dx` and `dy` are movements in those two directions. To move (1,2) by (3,4), return the new point (4,6).

The function receives a Point value and returns another Point. `return Point{..., ...};` creates the result in the same x-then-y order as the declaration. Add dx only to x and dy only to y. The supplied input and output code already reads and prints the members, so you do not need an extra display function.

Check no movement as well as positive and negative movement. A negative movement means subtracting in that direction; ordinary addition with a negative value already handles it. Class templates appear in the later sequence; you do not need template syntax to use these records.

- [Scoped enums](https://www.learncpp.com/cpp-tutorial/scoped-enumerations-enum-classes/)
- [Structs](https://www.learncpp.com/cpp-tutorial/introduction-to-structs-members-and-member-selection/)

- [Worked example](activities/13-records/worked-example.yaml)
- [Step through](activities/13-records/macro-visualization.yaml)
- [Arrange code](activities/13-records/parsons-puzzles.yaml)
- [Fill gaps](activities/13-records/code-completion.yaml)
- [Explain why](activities/13-records/multiple-choice-question.yaml)
- [Predict output](activities/13-records/parameterized-code-tracing.yaml)
- [Write code](activities/13-records/free-coding.yaml)

## 14. Classes protect their invariants

### Let an object protect its own rules
A class combines stored information with operations that use it. In Counter, the integer `value_` is private: outside code must use the public operations rather than changing it directly. The trailing underscore is simply a naming choice to distinguish stored members from parameters.

An **invariant** is a rule that should keep holding for a valid object. The Counter in the coding task starts nonnegative and accepts only positive additions. Its add operation protects that rule instead of relying on every caller to remember it.

### Read the class from the inside out
```cpp
explicit Counter(int start) : value_{start} {}
void increment() { ++value_; }
int value() const { return value_; }
```

The constructor has the class name and prepares a new Counter. The part `: value_{start}` initializes the stored member from start before the body runs. `explicit` prevents an integer from being silently turned into a Counter in other contexts; here construction is written out clearly as `Counter counter{3};`.

`increment()` is a member function: `counter.increment()` acts on counter. It returns no number because its result is the changed object. `value()` returns the stored count. The const after its parentheses promises it will not change this object's ordinary stored members, so it can be used when the object is being observed through a const reference.

### Your coding task: control a requested addition
The supplied add method receives amount. Add it only when it is greater than zero; ignore zero and negative requests. Do not reset the stored value or print from the method. main calls the method, then prints through the observer. The const reference named observed in main is another way to read the same object, not a second counter.

The example and Step through show a valid update. Fill gaps and Arrange code connect creating an object, using its operation, and reading the new value. Predict output changes the requested update, so check its rule before changing your state table.

When an object reaches the end of its lifetime, its destructor runs. Our Counter owns no outside resource and needs no custom destructor. Later modules use library ownership types to release resources automatically. For now, concentrate on the public rule and the one private value that enforces it.

- [Encapsulation](https://www.learncpp.com/cpp-tutorial/the-benefits-of-data-hiding-encapsulation/)
- [Constructors](https://www.learncpp.com/cpp-tutorial/constructor-member-initializer-lists/)
- [Destructors](https://www.learncpp.com/cpp-tutorial/introduction-to-destructors/)

- [Worked example](activities/14-classes/worked-example.yaml)
- [Step through](activities/14-classes/macro-visualization.yaml)
- [Arrange code](activities/14-classes/parsons-puzzles.yaml)
- [Fill gaps](activities/14-classes/code-completion.yaml)
- [Explain why](activities/14-classes/multiple-choice-question.yaml)
- [Predict output](activities/14-classes/parameterized-code-tracing.yaml)
- [Write code](activities/14-classes/free-coding.yaml)

## 15. Vectors, arrays, iterators, and algorithms

### A vector owns a list of values
`std::vector<int>` is a resizable list of integers. Include `<vector>` to use it. `std::vector<int> values{5, 1, 3};` creates three elements. A vector's **size** is the number of existing elements. Its **capacity** is the space available before another allocation is needed.

`reserve(10)` makes room for future elements; it does not create ten elements. `resize(10)` changes the number of existing elements. Explain why asks about this difference. A fixed-size `std::array` is another owning container for a size that stays known in advance; these activities use vectors.

### Sort a complete range
```cpp
std::sort(values.begin(), values.end());
```

`std::sort`, supplied by `<algorithm>`, puts the selected values in increasing order. `begin()` marks the first element. `end()` marks a position just after the last element. Together they describe a range that includes the beginning and excludes the end. Do not try to read an element at end.

### Visit each element without keeping an index
`for (int value : values)` visits each element by value. Each visit gets a temporary copy named value. `for (int& value : values)` instead lets a visit change the actual element. The supplied input loop in the coding task uses references to fill the vector. Your counting loop only needs to read, so a copy of each small integer is fine.

main first reads n, creates n elements with `std::vector<int> values(n)`, and fills them. This form uses parentheses because n is the number of elements, not a single element to put in the list. Inputs keep n nonnegative and small.

### Count what meets a rule
Write code supplies `countPositive(const std::vector<int>& values)`. The const reference lets the function read the existing list without copying the entire vector or changing its elements. Begin a count at zero, visit every value, and increase the count only for values greater than zero. Return the count after the loop.

The example and puzzle sort; the prediction and visualization count qualifying values in a short list. Both use the same habits: visit the intended elements, keep the accumulating result separate, and handle an empty list without reading an element that is not there.

- [Vectors](https://www.learncpp.com/cpp-tutorial/introduction-to-stdvector-and-list-constructors/)
- [Range loops](https://www.learncpp.com/cpp-tutorial/range-based-for-loops-for-each/)
- [Algorithms](https://www.learncpp.com/cpp-tutorial/introduction-to-standard-library-algorithms/)

- [Worked example](activities/15-containers/worked-example.yaml)
- [Step through](activities/15-containers/macro-visualization.yaml)
- [Arrange code](activities/15-containers/parsons-puzzles.yaml)
- [Fill gaps](activities/15-containers/code-completion.yaml)
- [Explain why](activities/15-containers/multiple-choice-question.yaml)
- [Predict output](activities/15-containers/parameterized-code-tracing.yaml)
- [Write code](activities/15-containers/free-coding.yaml)

## 16. Dynamic lifetime, recursion, and lambdas

### Keep a small function as a value
A **lambda** is a small function written where it is needed. You can store it in a variable and call it later. In this example, value is its ordinary parameter; bonus comes from the surrounding function.

```cpp
auto addBonus{[bonus](int value) { return value + bonus; }};
```

The capture list `[bonus]` stores a copy of bonus when this lambda is created. Changing the original bonus later does not change that saved copy. `[&bonus]` would instead refer to the original integer and see later changes, as long as that integer remains alive. An empty capture list `[]` does not make the local bonus available to the body.

The worked example changes the original bonus before calling addBonus. Step through and Predict output ask you to keep the saved copy and the original in separate rows. The puzzle puts creation of that copy before the later change. This order explains the result; it is not an arbitrary code arrangement.

### A function can call itself on a smaller problem
**Recursion** means a function calls itself. To calculate a sum through n, it can add n to the sum through n − 1. Every call has its own n. A base case supplies an answer without another call: for a sum through zero, that answer is zero.

For a sum through 3, think “3 plus the sum through 2,” then “2 plus the sum through 1,” and finally reach zero. After reaching the base case, the answers come back up through the waiting calls. Each step needs both a stopping rule and progress toward it. A base case written after an unconditional recursive call comes too late.

### Your coding task
Complete sumTo for inputs from 0 to 100. Handle zero directly, then make the remaining case smaller. Keep printing in main, after the function has returned the completed sum. The range keeps the number of calls and the resulting integer small enough for this exercise.

### Where storage fits
The wider reading distinguishes automatic objects, whose lifetimes follow a scope, from dynamically created objects, whose owner must arrange cleanup. We do not use raw new/delete in this module's exercises; the next module introduces a library owner. The important shared habit is to ask what a function retains and whether that retained object is still alive when the function uses it.

- [Dynamic allocation](https://www.learncpp.com/cpp-tutorial/dynamic-memory-allocation-with-new-and-delete/)
- [Recursion](https://www.learncpp.com/cpp-tutorial/recursion/)
- [Lambdas](https://www.learncpp.com/cpp-tutorial/introduction-to-lambdas-anonymous-functions/)

- [Worked example](activities/16-callables-memory/worked-example.yaml)
- [Step through](activities/16-callables-memory/macro-visualization.yaml)
- [Arrange code](activities/16-callables-memory/parsons-puzzles.yaml)
- [Fill gaps](activities/16-callables-memory/code-completion.yaml)
- [Explain why](activities/16-callables-memory/multiple-choice-question.yaml)
- [Predict output](activities/16-callables-memory/parameterized-code-tracing.yaml)
- [Write code](activities/16-callables-memory/free-coding.yaml)

## 17. Value operators, ownership, and relationships

### Give an object one clear owner
Some objects are created dynamically and need an owner that will release them when they are no longer needed. `std::unique_ptr<int>` is a library type that owns one integer exclusively. `<memory>` supplies it and its creation helper.

```cpp
auto original{std::make_unique<int>(7)};
auto owner{std::move(original)};
```

`make_unique<int>(7)` creates an integer holding seven and returns its unique owner. The second line transfers ownership into owner. `<utility>` supplies `std::move`; it permits this transfer rather than making a forbidden copy of unique ownership. After moving this unique_ptr, original is empty (`nullptr`). `*owner` reads the still-live owned integer.

Only one owner releases this integer. You do not write delete yourself. This is resource management tied to object lifetime, often called RAII: when the owner is destroyed, it releases what it owns. A moved unique_ptr becomes empty, but do not generalize that exact post-move state to every other C++ type.

Step through draws ownership labels, not raw memory addresses. The puzzle orders creating, moving, and observing the owner. Predict output varies the stored integer; moving its owner does not change that integer's value. Explain why asks which object is responsible for it after the transfer.

### Give a value type a familiar operation
The coding task is about a separate but related design choice: Score is a small value record. `operator+` is a function with a special name that makes `a + b` work for two Scores. Its two const-reference parameters let it read the original records without changing them. Return a **new** Score containing the sum of their points.

The supplied output prints the result followed by both originals. That checks not only addition but also the promise that the operands survive unchanged. Do not assign the sum back into a or b.

### Owning parts and borrowing access
Composition means a whole object owns its parts and manages their lifetime. Other relationships can refer to independently owned objects. Shared ownership has different costs and rules; it should describe an actual shared lifetime need. The wider readings introduce those designs, while these activities keep the ownership story deliberately simple and explicit.

- [Operator overloading](https://www.learncpp.com/cpp-tutorial/introduction-to-operator-overloading/)
- [Unique ownership](https://www.learncpp.com/cpp-tutorial/stdunique_ptr/)
- [Composition](https://www.learncpp.com/cpp-tutorial/composition/)

- [Worked example](activities/17-ownership/worked-example.yaml)
- [Step through](activities/17-ownership/macro-visualization.yaml)
- [Arrange code](activities/17-ownership/parsons-puzzles.yaml)
- [Fill gaps](activities/17-ownership/code-completion.yaml)
- [Explain why](activities/17-ownership/multiple-choice-question.yaml)
- [Predict output](activities/17-ownership/parameterized-code-tracing.yaml)
- [Write code](activities/17-ownership/free-coding.yaml)

## 18. Inheritance and virtual dispatch

### Use a general interface for a more specific object
Inheritance lets a derived type extend a base type. `struct Derived : Base` says that a Derived includes a Base part. In the example, Base supplies a general value operation and Derived supplies a more specific one.

```cpp
virtual int value() const { return 1; }
int value() const override { return 2; }
```

`virtual` in the base makes a call through a base reference choose the operation for the actual object. `override` in the derived declaration asks the compiler to check that it really replaces a base virtual operation with a matching signature. Keep the trailing const in both signatures; removing it changes the operation being declared.

`const Base& base{derived};` refers to the same Derived object through the general Base interface. The reference does not copy or change the object. Its name and declared type are general, but the actual object is still Derived. Step through and Predict output follow this exact distinction.

### Why a value copy is different
Creating a Base variable by copying a Derived keeps only the Base part. This is called slicing. The new object is a Base; it does not secretly keep being a complete Derived. Explain why asks about this difference between referring to an existing object and constructing a new base value.

### Your rectangle supplies a promised operation
The coding task's Shape declares `virtual int area() const = 0;`. The `= 0` means derived classes must provide this operation; it is not a returned zero. Rectangle supplies its override. Its constructor saves the input dimensions in width_ and height_. Complete the return calculation for area, width times height. main deliberately calls through a `const Shape&`, so the inherited interface is part of the test.

The line `virtual ~Shape() = default;` declares a virtual destructor. `~Shape` names cleanup at the end of an object's lifetime; `= default` asks the compiler to supply its normal implementation. Virtual cleanup supports safely destroying derived objects through a base owner. Our examples keep objects local, but the interface demonstrates this useful habit without requiring manual allocation.

The puzzle connects creating a specific object, binding the general reference, and making the virtual call. The class definitions are supplied and visible; there is no missing implementation outside the activity.

- [Inheritance](https://www.learncpp.com/cpp-tutorial/basic-inheritance-in-c/)
- [Virtual functions](https://www.learncpp.com/cpp-tutorial/virtual-functions/)
- [Virtual destructors](https://www.learncpp.com/cpp-tutorial/virtual-destructors-virtual-assignment-and-overriding-virtualization/)

- [Worked example](activities/18-polymorphism/worked-example.yaml)
- [Step through](activities/18-polymorphism/macro-visualization.yaml)
- [Arrange code](activities/18-polymorphism/parsons-puzzles.yaml)
- [Fill gaps](activities/18-polymorphism/code-completion.yaml)
- [Explain why](activities/18-polymorphism/multiple-choice-question.yaml)
- [Predict output](activities/18-polymorphism/parameterized-code-tracing.yaml)
- [Write code](activities/18-polymorphism/free-coding.yaml)

## 19. Class templates and specialization

### Turn a class design into a reusable pattern
A class template applies the template idea from functions to a whole type. In `template <typename T> class Box`, T stands for the chosen member type. `Box<int>` stores an integer; `Box<double>` stores a double. They are different types produced from the same pattern.

```cpp
template <typename T>
class Box {
    T value_;
public:
    explicit Box(T value) : value_{value} {}
    T value() const { return value_; }
};
```

The constructor receives a T and initializes the stored T member. The observer returns a T and leaves the object unchanged. The same source pattern preserves the different value types; it does not convert every member to an integer. Explain why asks you to distinguish sharing a pattern from being the same instantiated type.

### Follow one object at a time
The example creates one integer box and one fractional box. The puzzle orders construction, observation, and printing for one box. Step through and Predict output vary an integer stored in the box. There is no automatic doubling, clearing, or type conversion when value() is called: the observer simply returns the stored value.

### Your class holds a pair
The supplied Pair<T> class has two private members, first_ and second_. Its constructor has already stored the two arguments. Complete the const sum observer so it returns their sum as a T. main checks an input Pair<int> and a fixed Pair<double>. A solution using an integer-only local or return type could lose the fractional part and violate the pattern's promise.

### Two extensions in the reading
A non-type template parameter supplies a build-time value rather than a type, for example the fixed element count in `std::array<int, 3>`. An ordinary number read from input cannot take that build-time role.

Specialization supplies a particular implementation for selected template arguments. It is useful when the general pattern does not fit a special type, rather than merely to repeat the same code. These are follow-up reading ideas; every activity here practices the general class pattern so you can understand it before choosing special cases.

When describing a box, say its complete type—Box<int> or Box<double>—and trace its own stored value. That habit prevents confusing the template's placeholder name with a single shared object or one universal storage type.

- [Class templates](https://www.learncpp.com/cpp-tutorial/template-classes/)
- [Non-type parameters](https://www.learncpp.com/cpp-tutorial/template-non-type-parameters/)

- [Worked example](activities/19-class-templates/worked-example.yaml)
- [Step through](activities/19-class-templates/macro-visualization.yaml)
- [Arrange code](activities/19-class-templates/parsons-puzzles.yaml)
- [Fill gaps](activities/19-class-templates/code-completion.yaml)
- [Explain why](activities/19-class-templates/multiple-choice-question.yaml)
- [Predict output](activities/19-class-templates/parameterized-code-tracing.yaml)
- [Write code](activities/19-class-templates/free-coding.yaml)

## 20. Exceptions and stream-based I/O

### Report a failure without inventing a normal result
An exception signals that an operation could not complete normally. The example's checkedDivide returns an integer quotient for a nonzero denominator. If the denominator is zero, it throws an `std::invalid_argument` exception instead of attempting invalid division. `<stdexcept>` supplies this standard error type.

```cpp
try {
    std::cout << checkedDivide(12, 0) << '\n';
} catch (const std::exception& error) {
    std::cout << error.what() << '\n';
}
```

`try` surrounds work that may fail. A matching `catch` handles a thrown exception. The const reference observes the actual exception without copying it. `what()` supplies its message. When a call throws, execution does not continue at the next instruction inside that try block; control goes to the handler.

As control leaves scopes while searching for a handler, fully constructed local objects are destroyed. This cleanup is called stack unwinding. It is why the automatic owners from the earlier module help even when a calculation fails. Explain why asks about cleanup; the visualization and prediction follow the chosen exception path.

### Apply the input-stream tools to a stored line
The coding task uses `std::istringstream`, supplied by `<sstream>`, to read fields from an existing string rather than directly from the keyboard. `std::getline` first obtains the line. `std::istringstream input{line};` gives a small stream the line to examine. The usual `input >> a >> b` then tries to read two integers in order.

Two successful reads are necessary but not sufficient. The task permits exactly two integer fields, so a third non-whitespace token is invalid. Try reading one more token into the supplied string extra. If that succeeds, reject the line. If it fails after both integers were read, only trailing whitespace remains and the record is complete. This also rejects `1 2x`: the leftover x is an extra token.

### Your validation order
First obtain both required fields. Only after that succeeds should you look for unwanted extra input. Logical AND short-circuits, so it can express that dependency. Print the sum for a complete valid record; otherwise print invalid. The supplied examples include a missing field and a trailing token to distinguish those situations.

File streams use a similar reading interface for files; their owners close files automatically. The linked file-I/O reading is a follow-up, not a hidden dependency on a file on your machine. These activities need only the text or values shown in the program.

- [Exceptions](https://www.learncpp.com/cpp-tutorial/basic-exception-handling/)
- [String streams](https://www.learncpp.com/cpp-tutorial/stream-classes-for-strings/)
- [File I/O](https://www.learncpp.com/cpp-tutorial/basic-file-io/)

- [Worked example](activities/20-exceptions-streams/worked-example.yaml)
- [Step through](activities/20-exceptions-streams/macro-visualization.yaml)
- [Arrange code](activities/20-exceptions-streams/parsons-puzzles.yaml)
- [Fill gaps](activities/20-exceptions-streams/code-completion.yaml)
- [Explain why](activities/20-exceptions-streams/multiple-choice-question.yaml)
- [Predict output](activities/20-exceptions-streams/parameterized-code-tracing.yaml)
- [Write code](activities/20-exceptions-streams/free-coding.yaml)

## Capstone: a small stock controller
After module 14.

### A small inventory with one clear rule
An inventory stores a nonnegative number of items. Its class already has a constructor and a stock observer. You write two public actions. Each action first decides whether a request is allowed, then either changes the stock once or rejects the request without changing anything.

`add(amount)` accepts only a positive amount. `take(amount)` also requires that the stock can cover the full amount. For both actions, return true when accepted and false when rejected. This return value is separate from the stored stock: main prints both the decision and the new stock after each command.

### Read the supplied caller
Input begins with initial stock and the number of commands. Each later command is add or take followed by its amount. The loop reads one command at a time. Its conditional expression chooses the matching method. The output uses the returned bool to select ok or rejected, then reads the current stock through the observer. You do not need to change this caller.

### Work in two passes
Complete add first and test a positive, zero, and negative amount. Then complete take and test a small permitted withdrawal, an exact-stock withdrawal, an overdraft, and a zero/negative request. Keep your rejection checks before the update so a failed request cannot change the state.

The two highlighted editor regions are independent method bodies. The read-only surrounding code supplies the names and input/output. In a no-commands case no transaction result is printed; an empty output is correct.

[Open project](activities/capstone-01-stock/free-coding.yaml)

## Capstone: validated score reports
After module 20.

### Turn complete text records into a useful report
Each record is one name and one score. Record is a supplied struct with those two named members. The input starts with a line count, followed by that many complete record lines. Names are single words. main already reads the line count, discards the newline left by that numeric read, and obtains each following line with getline. You do not need a file on disk.

### First marked region: parse one line
Build an istringstream from the supplied line. Read into a temporary Record named candidate so a failed parse cannot partly change the caller’s result. Require a name and an integer score, reject scores outside 0–100, and reject an extra non-whitespace token. Only after all checks succeed should you assign result and return true. Otherwise return false; main prints invalid and stops.

### Second marked region: summarize valid records
printReport receives a const reference to the vector that main has built. Count is its size. Add all scores and divide by the count using a double calculation; for an empty vector use 0.0 instead of dividing by zero. fixed and setprecision(1) give the requested one-decimal display.

Use a pointer named best to refer to a record already in that vector. Start it at nullptr. As you visit each const Record&, replace best only when no best exists yet or the current score is strictly higher. A strict comparison preserves the first record in a tie. Because the vector is not changed while reporting, these references stay valid.

### Explain the edge cases before coding
For no records, print count 0, average 0.0, and best none on separate lines. For a tie, keep the first highest-scoring name. A readable score followed by an extra character is not a complete valid record. The test examples below connect each of these rules with concrete input and output. Edit the two marked regions; the surrounding input loop and output contract are supplied.

[Open project](activities/capstone-02-report/free-coding.yaml)
