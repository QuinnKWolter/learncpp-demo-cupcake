"""One-time, reproducible editorial migration. Future authoring uses content/modules/*.yaml.

The preserved v1 source is only a migration input. The generated module YAML is the
single source read by the course builder after this revision.
"""
from pathlib import Path
from textwrap import dedent
import importlib.util
import copy
import yaml

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('course_v1',ROOT/'research/course-v1-source.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
MODULES=copy.deepcopy(old.MODULES);CAPSTONES=copy.deepcopy(old.CAPSTONES)

def code(s):return dedent(s).strip()+'\n'
def revise(n,lesson,*,completion,reason,write,arrange,trace,explain,success,**changes):
    m=MODULES[n-1];m.update(changes)
    m['lesson']=dedent(lesson).strip()
    m['hints_by_type']={'code-completion':completion,'multiple-choice-question':reason,
                        'free-coding':write,'parsons-puzzles':arrange,'parameterized-code-tracing':trace}
    m['explanations']=explain
    m['completion_explanation']=success
    m['review_note']='Reviewed for prerequisites, plain-language guidance, feedback, boundary cases, and C++23.'

def puzzle(n,source,blocks,goal,hints=None,groups=None,stdin=''):
    m=MODULES[n-1]
    m['puzzle']=dict(source=code(source),blocks=[dict(snippet=s,explanation=e) for s,e in blocks],
                     goal=goal,stdin=stdin,groups=groups or {})
    if hints:m['hints_by_type']['parsons-puzzles']=hints

def tracing(n,source,token,values,goal,steps,output,*,expected,context=None,stdin=''):
    """Authored states describe the FIRST parameter value; variants have independent oracles."""
    m=MODULES[n-1]
    m['tracing']=dict(source=code(source),token=token,values=values,goal=goal,stdin=stdin,
                      context=context,walkthrough=[dict(snippet=s,note=note,state=state) for s,note,state in steps],output=output,expected=expected)

revise(1,r'''
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
''',
 completion=['Ask what “four groups of three” means. Which operation combines equal-sized groups?', 'Addition would count the two labels once each. Think about counting every item inside every box.'],
 reason=['Compare `int n{};` with a declaration that gives n an explicit starting number.', 'Empty braces have a specific meaning for an integer: they provide a starting value even without input.'],
 write=['Try the task by hand for n = 3 and n = −3. In both cases multiply the input by itself.', 'Use the existing n twice in one expression, send that result to std::cout, and finish the line. You do not need to change the input code.'],
 arrange=['A variable must exist before a calculation can use it. Find the two starting quantities first.', 'The total needs both quantities. Printing needs the total. Which steps therefore have to come earlier?'],
 trace=['Write down the displayed boxes value and the fixed perBox value before doing arithmetic.', 'There is only one output statement. Multiply the two current values and write that one number.'],
 explain=[('int boxes{4};','Start here: boxes now holds 4. The braces give it that value before the calculation uses it.'),('int perBox{3};','perBox means “items in one box.” It holds 3; it is a different quantity from the number of boxes.'),('int total{boxes * perBox};','Count equal groups by multiplying. The result is stored in total; boxes and perBox keep their values.'),(r"std::cout << total << '\n';",'Read this as “print total, then start a new line.” It prints the stored answer rather than recalculating or changing it.')],
 success='Multiplication counts every item in every box. Adding the quantities would count boxes and items-per-box as though they were the same kind of thing.',
 region_prompts=['Calculate the square of n and print it, followed by a newline.'])

revise(2,r'''
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

The complete function definition is visible below `main` in the program. There is no missing pricing function, hidden calculation, or extra file for you to invent. Both files travel with the activity and are supplied to the compiler when you check an answer.

### Follow a call and come back
For width 3 and height 5, enter the function, calculate `2 * (3 + 5)`, and return to the output line. The parameters belong to this call; another call can use different dimensions. This same call-and-return sequence is shown in Step through and Predict output.

### Use the idea in a new task
Write code asks for **area**, the number of unit squares inside a rectangle, rather than perimeter. Area is `width * height`. The function name, parameters, input, and output lines are supplied. Write only the return calculation. Check a rectangle and a square: the same formula must work for both. Never print from the function just to display the answer; the supplied `main` already does that.
''',
 completion=['Locate the function body below main. The missing expression must calculate distance around all four sides.', 'A rectangle has two sides of each dimension. Add one width and one height, then account for the second pair.'],
 reason=['Separate two actions: returning a value to another part of the program and displaying text on the screen.', 'The caller decides what to do with the returned number. Look for std::cout when deciding what actually gets printed.'],
 write=['This task asks for area, not the perimeter in the example. Draw a rectangle with 3 rows of 5 squares.', 'Return one multiplication using the two parameter names. The supplied caller reads the dimensions and prints the returned value.'],
 arrange=['A call can only use values already created. Look for the dimension declarations before the call.', 'After the call returns, its result can be printed. The function declaration and definition are already supplied around the movable part.'],
 trace=['Copy the displayed width and the fixed height into the function parameters for this call.', 'Calculate inside the function first. Then put its returned number into the output line; return itself does not create another output line.'],
 explain=[('#include "geometry.hpp"','This supplied header announces rectanglePerimeter before main calls it. Open the supporting file to see the short declaration.'),('rectanglePerimeter(width, height)','Pass the two values to the named calculation. This expression becomes the number that the function returns.'),('int rectanglePerimeter(int width, int height) {','This is the definition. For each call, width and height receive that call’s two arguments.'),('return 2 * (width + height);','First add one width and one height, then double that sum to count all four sides. Send that answer back to main; main prints it.')],
 success='The perimeter counts both pairs of sides. Multiplying width by height calculates area instead; adding only once counts only half the boundary.',
 example=code(r'''
 #include <iostream>
 #include "geometry.hpp"
 int main() {
     int width{3};
     int height{5};
     std::cout << rectanglePerimeter(width, height) << '\n';
 }
 int rectanglePerimeter(int width, int height) {
     return 2 * (width + height);
 }
 '''), includes={'geometry.hpp':code('''
 // A declaration announces this function before main calls it.
 // Its definition (the calculation) is visible in main.cpp.
 #ifndef CUPCAKE_GEOMETRY_HPP
 #define CUPCAKE_GEOMETRY_HPP
 int rectanglePerimeter(int width, int height);
 #endif
 ''')},blank='2 * (width + height)',wrong=[('width * height','This calculates the area inside the rectangle. Perimeter counts the boundary: two widths and two heights.'),('width + height','You have counted one width and one height. The opposite two sides still need to be counted.')],
 task='A rectangle’s area is width × height. Complete `rectangleArea(int width, int height)` by returning that area. The supplied code reads two whole numbers from 1 to 1000 and prints the returned result. Edit only the marked function body; it should return a number, not print it.',
 solution=code(r'''
 #include <iostream>
 int rectangleArea(int width, int height) {
     return width * height;
 }
 int main() {
     int width{}, height{};
     std::cin >> width >> height;
     std::cout << rectangleArea(width, height) << '\n';
 }
 '''),editable='    return width * height;',cases=[('Rectangle','3 5\n','15\n'),('Square','4 4\n','16\n'),('Thin rectangle','1 9\n','9\n'),('Larger dimensions','1000 2\n','2000\n')],
 region_prompts=['Return the area using the width and height parameters.'])

revise(3,r'''
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
''',
 completion=['At the final assignment, left already holds the old right value. Which name still keeps the old left value?', 'Think about the purpose of saved: it protects a value that the next assignment would otherwise overwrite.'],
 reason=['A useful test must make it possible to tell the two original values apart.', 'Imagine swapping two identical labels. Would the final display reveal whether either label really moved?'],
 write=['Write down what must survive before your first assignment. Store the old a value in a separate integer.', 'Use that saved original value for the final assignment, after a has received b. The supplied output line shows whether both originals survived.'],
 arrange=['Find the block that preserves the original left value. It must happen before left changes.', 'Printing belongs after both assignments; otherwise you would display a partly finished swap.'],
 trace=['Use a small table with a column for each variable. Change only one column at each assignment.', 'When you read right = saved, use saved’s current value—not the new value of left.'],
 explain=[('int left{2}, right{9};','These are the two original values. We want them in opposite places at the end.'),('int saved{left};','Keep a copy of the old left value before anything overwrites left.'),('left = right;','Only left changes here. right still holds its original value.'),('right = saved;','Recover the preserved old left value. Both originals now survive, in their new places.')],
 success='The saved value is the original left value. Using left here would copy the already changed value and lose one of the two originals.',region_prompts=['Swap a and b, preserving the original a in a temporary integer.'])

revise(4,r'''
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
''',
 completion=['Look at the operand types immediately before division. Are both still integers?', 'The conversion must happen before the fractional part is lost. Converting a finished integer quotient cannot bring it back.'],
 reason=['Evaluate the expression inside the braces first, using the types of 7 and 2.', 'Only after that expression finishes is its result used to initialize the double. Which information has already been discarded?'],
 write=['Try scores 7 and 8 by hand. The total is odd, so an integer division would lose half a point.', 'Convert the total to double before dividing by two. Leave the supplied one-decimal-place output code as it is.'],
 arrange=['The total and count must exist before they can be used in the quotient.', 'Make the fractional calculation before printing it; a display setting alone cannot fix integer division.'],
 trace=['First work out which division uses two integers. Then find the division with a double operand.', 'Track both results separately and preserve the space between them in the output.'],
 explain=[('int sum{15}, count{4};','Both starting values are integers. Their types matter to the division.'),('static_cast<double>(sum)','For this calculation, use a double version of sum. The original sum is still an int.'),('sum / count','This second expression still has two int operands, so it drops the fractional part before printing.')],
 success='The conversion supplies a double operand before division. Without it, the calculation discards the fraction; the destination variable cannot recover it.',
 region_prompts=['Calculate mean without losing a possible half point.'])

revise(5,r'''
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
''',
 completion=['“Contains” means anywhere in the text, not only at the beginning.', 'The word cupcake ends with cake. A beginning-only check and an empty-string check ask different questions.'],
 reason=['Ask who actually stores the characters: the string, or the view looking at it?', 'A view does not make its own copy. Its usefulness depends on the original characters still being available.'],
 write=['Read the entire line before measuring it. An input like Ada Lovelace contains a space that should count.', 'getline leaves the ending newline out of the string. Its size therefore already matches the requested character count.'],
 arrange=['Create the text before asking a question about its characters.', 'The printed result comes from the text operation, so the question must be evaluated before its result is sent to output.'],
 trace=['Use the text shown in your version of the program. Count its letters and spaces, not its quote marks.', 'The ending newline is an output instruction, not another character inside the stored word.'],
 explain=[('const std::string word{"cupcake"};','word owns these seven characters. const tells us that this example will not change them.'),('word.contains("cake")','Search anywhere in cupcake for the sequence cake. This is a C++23 string operation.'),('std::boolalpha','Display a true/false answer as words so it is easier to read.')],
 success='contains searches the whole string. A word can contain cake even though it begins with cup, so starts_with would answer a different question.',
 example=code(r'''
 #include <iostream>
 #include <string>
 int main() {
     const std::string word{"cupcake"};
     std::cout << std::boolalpha << word.contains("cake") << '\n';
 }
 '''),blank='word.contains("cake")',wrong=[('word.starts_with("cake")','This checks only the beginning. Cupcake begins with cup, but cake still appears later in the word.'),('word.empty()','This asks whether there are no characters. It does not search for the requested letters.')],
 region_prompts=['Read the whole input line, then print its character count.'])

revise(6,r'''
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
''',
 completion=['Try an age just outside the group, such as 11. Which comparison fails, and should that be enough to reject it?', 'The range has two requirements, not two alternative ways to qualify. Choose an operator that requires both.'],
 reason=['Follow C++ evaluation from left to right for the first comparison. What kind of value does a comparison produce?', 'The second comparison receives true or false, not the original n. Write two separate comparisons joined by AND instead.'],
 write=['List the three checks in words before writing symbols: lower bound, upper bound, evenness.', 'An even number outside the interval must still be rejected. Join all three checks so none can be skipped as an alternative.'],
 arrange=['Read the starting value, calculate the decision, then print that decision.', 'Use the Boolean variable after the declaration that creates it. The output line should not come before its value has been decided.'],
 trace=['Evaluate each age comparison separately. Write T or F beside each before combining them.', 'For AND, one false comparison makes the whole result false. The output is a word because boolalpha is supplied.'],
 explain=[('std::cin >> age;','The initial 16 is replaced by the supplied input for this run. Check the sample input before predicting the result.'),('age >= 12 && age <= 17','Ask both range questions. Ages 12 and 17 are included because each comparison permits equality.'),('std::boolalpha','The resulting bool is printed as true or false instead of as a digit.')],
 success='AND requires both ends of the range to hold. OR would let an out-of-range value pass merely because it satisfies the other bound.',
 region_prompts=['Set accepted to true only when n meets both bounds and is even.'])

revise(7,r'''
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
''',
 completion=['Compare a fresh counter on each call with one counter that remembers the last issued number.', 'The initializer should run once, while the name remains inside the function. Which declaration gives that combination?'],
 reason=['Treat “where can I name it?” and “when is it destroyed?” as two separate questions.', 'A static local is the example that separates them: a local name, but a value that survives a return.'],
 write=['Do the conversion by hand: two hours contains twice as many minutes as one hour.', 'The namespace and function signature are supplied. Return hours multiplied by the minutes in one hour; main already prints it.'],
 arrange=['Create the call sequence in the same order that tickets should be issued.', 'The static counter belongs inside nextTicket. In main, each call should finish before the following result is printed.'],
 trace=['After a call returns, keep the ticket value in your table rather than resetting it to zero.', 'Prefix ++ changes the stored value before returning it. Apply that once for each displayed call.'],
 explain=[('static int ticket{0};','Create this counter once. Later calls keep using the value it has reached.'),('return ++ticket;','Increase the remembered count, then give that new number back to the caller.'),("std::cout << nextTicket() << ' ';",'This first call completes before the following output statement begins. Its space separates the two printed tickets.')],
 success='static preserves the counter between calls while keeping its name local. An ordinary local would start at zero again on every call.',
 task='Complete `toMinutes(int hours)` inside the supplied namespace `units`. One hour contains 60 minutes. Input is a whole number of hours from 0 to 1000; the supplied caller prints the returned number of minutes. Edit only the marked return calculation.',
 region_prompts=['Return the number of minutes in the given hours.'])

revise(8,r'''
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
''',
 completion=['The goal includes the limit itself. Check what the condition does when i equals limit.', 'Compare the totals for limit 1. The loop should still add that one allowed value.'],
 reason=['List the i values that satisfy the condition, starting with the declared initial value.', 'The condition is tested before each body execution. Stop listing as soon as i is no longer less than three.'],
 write=['Start with a running total of zero. What is the first positive even number you could add?', 'Advance the candidate by two each time and include n when it is even. Keep printing outside the loop so there is only one output line.'],
 arrange=['A running total needs its starting value before the loop begins.', 'The final output uses the completed total, so it belongs after the whole loop block.'],
 trace=['Make columns for i and total. Update total inside the body, then update i before the next test.', 'For limit zero, the first condition already fails. For other limits, include the last value only if it still passes <=.'],
 explain=[('int total{0};','Before any values are added, the sum is zero. This line runs once, outside the loop.'),('for (int i{1}; i <= limit; ++i) {','Begin at one, include limit, and advance by one after each visit.'),('total += i;','Add the current i to everything collected so far; do not reset the total.'),(r"std::cout << total << '\n';",'Print once, after all loop visits have finished.')],
 success='The inclusive condition allows the final value to contribute. A strict less-than test would miss that last contribution.',
 region_prompts=['Use a loop to add the positive even values up to n into total.'])

revise(9,r'''
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
''',
 completion=['A parsed score of zero and a parsed score of 100 are both valid. Check both endpoints.', 'The range test must include equality and must require both bounds, not just either one.'],
 reason=['User input can be wrong during normal use. Its error handling must still work in a release build.', 'Assertions can be turned off. Use regular validation to decide what message a user should receive.'],
 write=['Sort the situations into three groups before writing code: invalid input, valid passing score, valid retry score.', 'Handle a failed read or bad range first. Only then test whether the valid score reaches 60; the final else covers the remaining valid scores.'],
 arrange=['Reject invalid values before any branch can call them valid.', 'A successful conversion to int is only the first check. The allowed range is a separate decision.'],
 trace=['First decide whether the displayed score is inside the allowed range. If it is, choose the correct threshold branch.', 'Only one output branch is taken. Preserve the exact word selected by that branch.'],
 explain=[('!(std::cin >> score)','Try reading first. This condition becomes true if the input cannot be read as an integer.'),('return 0;','After reporting the bad read, stop main so the program does not continue with an untrusted value.'),('score >= 0 && score <= 100','A readable integer is acceptable only when it meets both bounds, including zero and 100.')],
 success='Both endpoints are valid, and both bounds must hold. Parsing an integer does not by itself establish that it is a permitted score.',
 region_prompts=['Read and validate score, then print exactly one of pass, retry, or invalid.'])

revise(10,r'''
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
''',
 completion=['Compare “convert, then divide” with “divide, then convert.” In which order can the half still survive?', 'The conversion needs to affect an operand of /. A double destination alone comes too late.'],
 reason=['Look only at the initializer 6, not at how the variable might be used later.', 'auto uses the type of that expression. A plain whole-number literal here has type int.'],
 write=['Use 9 and 2 as a trial input. The requested two-decimal answer needs to retain a half before formatting it.', 'Convert total before dividing by count. auto will then deduce the fractional result type.'],
 arrange=['The input values must be ready before you calculate the quotient.', 'Keep the conversion next to the numerator in the calculation, then print the completed result.'],
 trace=['Work out each division independently. One is entirely integer arithmetic; the other has a converted operand.', 'Write both results in output order with the separating space. Do not give the integer expression a fraction just because the next expression has one.'],
 explain=[('auto whole{9 / 2};','The initializer computes an integer quotient. auto therefore makes whole an int.'),('static_cast<double>(9) / 2','Convert the numerator first, so the division can keep its fractional part.'),('auto fraction','Because its initializer is a double expression, this variable is also a double.')],
 success='The operand conversion changes how division is performed. A conversion around a completed integer quotient would only convert the already truncated answer.',
 region_prompts=['Calculate average as a fractional quotient using auto.'])

revise(11,r'''
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
''',
 completion=['Read the expression as an if/else: when a < b, which variable is larger?', 'The true and false positions have different jobs. Test them with a small pair in increasing order, then with the order reversed.'],
 reason=['Compare a fixed literal used during a build with a value that arrives from std::cin during execution.', 'constexpr permits compile-time calculation when possible; an ordinary runtime call can still use the same function.'],
 write=['Use a small ordered pair such as 2 and 7 to decide which value belongs in each branch.', 'Then reverse the pair to check the other branch. Return the original T value so the fixed double example keeps its fractional part.'],
 arrange=['The values must exist before a call can receive them, and a result must be calculated before it can be printed.', 'The template definition is already supplied. You are ordering one caller’s steps, not arranging template syntax.'],
 trace=['Give a and b the displayed argument values, then evaluate a < b once.', 'Only the selected branch becomes the returned value; the two values are not added together.'],
 explain=[('template <typename T>','This function is a pattern. The call chooses the type represented by T.'),('a < b ? b : a','If a is smaller, choose b; otherwise choose a. This returns the larger value without changing either argument.'),('constexpr int best{larger(3, 8)};','This variable requires its initial value during the build, so this call is evaluated then.'),('larger(2.5, 1.5)','This call uses double for T. The function pattern also works without throwing away fractional information.')],
 success='When a < b, b is the larger value. Reversing the two result positions would correctly implement a smaller-value function, but not this larger-value function.',
 task='Complete the supplied function template `smaller(T a, T b)`. Return the smaller of a and b; do not print from the function. The caller reads two integers from −1000 to 1000 and also calls your function with 2.5 and 1.5. It prints the two results on one line. Keep the result type T so both integer and fractional values are handled.',
 region_prompts=['Return the smaller of a and b, preserving its type T.'])

revise(12,r'''
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
''',
 completion=['Ask whether addBonus should change a private copy or the caller’s actual score.', 'The body adds to score. A const reference would prevent that; a by-value parameter would change only a copy.'],
 reason=['Follow the local integer’s lifetime through the end of its function call.', 'Copying an address does not keep the addressed object alive. Ask whether there is still a valid object to use after return.'],
 write=['There are two cases: a negative value must change; zero or a positive value must stay as it is.', 'Use an if condition and assign through the supplied reference only in the negative case. The caller will observe that same integer.'],
 arrange=['Create a live integer before binding a reference to it.', 'A change through the reference affects that integer. Print after the change so the effect is visible.'],
 trace=['Draw one box for the integer and connect both the original name and its reference to it.', 'An assignment through the alias changes that one box. Read the original name from the updated box when printing.'],
 explain=[('int& score','This parameter is an alias for the caller’s score, so a change here is visible there.'),('score += 5;','Increase the shared integer by five; no second return value is needed.'),('int* pointer{&score};','Keep the address of the live score. This is a pointer to it, not a copy of its value.'),('*pointer','After checking for a non-null pointer, read the current integer at that address.')],
 success='The reference lets the function update the caller’s score. A value parameter would update only a copy; a const reference would prohibit this update.',
 task='Complete the action `clampToZero(int& value)`. Set a negative value to zero, and leave zero or a positive value unchanged. Input is one integer from −1000 to 1000. The caller passes its integer by reference and prints it after your function returns. Change only the marked body; the function returns no separate result.',
 region_prompts=['Change value to zero only if it is negative.'])

revise(13,r'''
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
''',
 completion=['Look at the status used when parcel is created. Which named status should the condition recognize?', 'Weight and status answer different questions. The decision asks whether this parcel is ready, not whether it weighs zero.'],
 reason=['Status names a type that owns the enumerator names, rather than an object with data members.', 'Use the same scope-separator idea as units::toMinutes. No call is needed to obtain a named enum value.'],
 write=['Keep the two directions separate: x changes by dx, and y changes by dy.', 'Construct the returned Point in its declared member order. Zero movement should return the original coordinates.'],
 arrange=['The record needs to exist before the program can inspect its members.', 'A test of status chooses whether to print the weight. Keep the print in the intended branch.'],
 trace=['Match the two initializers to the members in declaration order.', 'Select the status branch first. Only then decide which weight, if any, reaches the output statement.'],
 explain=[('enum class Status { waiting, ready };','Give the two allowed states meaningful names, kept inside Status’s scope.'),('Parcel parcel{4, Status::ready};','Initialize the record in declaration order: weight four, then ready status.'),('parcel.status == Status::ready','Compare this record’s stored choice with the ready value.'),('parcel.weight','Read the weight member from this particular parcel.')],
 success='The condition checks the parcel’s named status. Its numeric weight does not tell us whether it is ready.',
 region_prompts=['Return a new Point with x moved by dx and y moved by dy.'])

revise(14,r'''
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
''',
 completion=['An increment means one step upward from the current count, not a new starting value.', 'Use an operation that changes the stored value by one while preserving all earlier increments.'],
 reason=['If a caller could assign any value directly, could the class enforce its accepted-update rule?', 'Private storage makes callers request an operation. The method can check the request before changing that storage.'],
 write=['Decide whether the requested amount is allowed before changing value_.', 'A rejected zero or negative amount should leave the stored value exactly as it was. Update only in the positive branch.'],
 arrange=['Create a Counter before calling a member function on it.', 'Reading the count before increment would show the old value. Put the observer after the update when the task asks for the final count.'],
 trace=['Keep one row for the object’s stored value. Check the add method’s condition before updating it.', 'The observer returns what is currently stored; it does not add again or reset anything.'],
 explain=[('int value_{};','The stored count is private. The underscore is just a helpful naming convention.'),('explicit Counter(int start) : value_{start} {}','Construct a new counter by initializing its member from start; the body has no extra work.'),('void increment() { ++value_; }','An action on this object increases its stored count by one.'),('int value() const { return value_; }','Read the count without changing it. const describes the observer’s behavior on the object.')],
 success='Increment increases the existing count by one. Resetting it would discard its history; decrement would move it in the opposite direction.',
 region_prompts=['Accept a positive amount and update value_; leave it unchanged otherwise.'])

revise(15,r'''
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
''',
 completion=['Sort needs the start of the list and the position just beyond its final element.', 'A range that begins and ends at begin contains no elements. A range ending one element later is still too short for the whole vector.'],
 reason=['Distinguish making room from creating items. Which operation changes capacity without changing size?', 'After reserve, ask how many integers have actually been inserted or created. Empty reserved storage is not a list of elements yet.'],
 write=['Start count at zero and inspect each stored integer. Zero itself should not count as positive.', 'Increase count only in the value > 0 case, then return once the loop has finished. An empty list should naturally return the starting zero.'],
 arrange=['Create the vector before using begin and end to describe it.', 'The range loop prints the current order. Put sorting before it if the required display is sorted.'],
 trace=['Visit the displayed values in order, adding one to count only for a strictly positive value.', 'Keep zero separate from positive values. The final output is the count, not the sum of the positive values.'],
 explain=[('std::vector<int> values{5, 1, 3};','Create an owning list containing these three integers, in this order.'),('std::sort(values.begin(), values.end());','Sort every existing element. The end marker is just beyond the final element.'),('for (int value : values)','Read one element per loop visit; this loop does not change the vector.'),(r"std::cout << value << ' ';",'Print each visited value followed by a space. The later output line adds the ending newline.')],
 success='end marks the boundary after the last element, so the half-open range covers the entire vector. An earlier boundary would leave some values unsorted.',
 task='Complete `countPositive(const std::vector<int>& values)` by returning how many elements are greater than zero. The supplied caller reads n (0–100), then n integers (−100 to 100), and prints your returned count. Do not change the vector. Zero is not positive, and an empty vector should give a count of zero.',
 region_prompts=['Count the elements greater than zero, then return the count.'])

revise(16,r'''
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
''',
 completion=['Look at when the lambda is created and when bonus changes. Should its saved bonus follow that later change?', 'A value capture stores a copy at creation time. A reference capture follows the original instead. Choose the one that preserves the original bonus.'],
 reason=['The zero case must be reached without first making yet another recursive call.', 'Changing n toward zero is necessary, but at zero the function must return an answer directly. Check the order of those two decisions.'],
 write=['First decide what the sum should be when there is nothing to add. That case should return without calling sumTo again.', 'For a positive n, combine n with the sum for the smaller input n − 1. Eventually that smaller input reaches your stopping case.'],
 arrange=['Capture a value before changing the original if you want the function to retain the earlier value.', 'The later call uses whichever value was captured at creation. Put the final print after the original has changed so the difference is observable.'],
 trace=['Make separate rows for the original bonus and the copy kept by the lambda.', 'The later assignment changes only the original row. Add the call argument to the captured row when predicting output.'],
 explain=[('[bonus]','Capture a copy now. This is when the lambda stores the bonus it will use on later calls.'),('(int value) { return value + bonus; }','Each call supplies value; the body adds the separately captured bonus and returns the total.'),('bonus = 9;','Change the original variable. The earlier copy inside the lambda stays as it was.'),('addBonus(4)','Use four as the parameter and the captured bonus as the other operand.')],
 success='A value capture keeps the earlier bonus. Reference capture would make the same body observe the later assignment instead.',
 question='What makes a recursive sum through n stop correctly when n reaches zero?',
 choices=[('Return the zero-case answer before making another recursive call.','At zero there is no smaller sum to request. Returning directly lets the waiting calls finish.'),('Make the recursive call first, then check whether n is zero.','At zero that call happens before the check, so the intended stopping condition cannot stop it in time.'),('Keep calling the same function with the same n until it stops by itself.','Repeating an unchanged problem does not move toward a stopping case.')],
 task='Complete `sumTo(int n)` using recursion (a call to the same function with a smaller input). Return the sum of whole numbers from 1 through n. For n = 0, return zero without another call. Input is n from 0 to 100. The supplied main prints the returned sum once.',
 region_prompts=['Handle the zero case, then return n plus the smaller sum.'])

revise(17,r'''
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
''',
 completion=['unique_ptr represents one owner. Ask whether the second line should copy ownership or transfer it.', 'The original object should survive, but its responsible owner should change. Creating a different integer does not achieve that.'],
 reason=['Follow the ownership transfer, not just the address or stored number.', 'After a unique_ptr move, the source is empty and the destination is responsible for the original object.'],
 write=['The function should produce a new value while leaving both inputs alone. Read their points members and combine those numbers.', 'Use Score{...} to create the returned record. Do not update either const-reference operand; the caller prints them to check this promise.'],
 arrange=['An owner must exist before its ownership can be transferred.', 'Read through the destination after the transfer. The source unique_ptr is empty at that point.'],
 trace=['Keep two facts separate: which pointer owns the object, and what integer the object holds.', 'Moving this owner changes responsibility, not the stored integer. The original == nullptr question therefore has its own Boolean answer.'],
 explain=[('std::make_unique<int>(7)','Create an integer holding seven and one library object responsible for its lifetime.'),('std::move(original)','Permit the unique ownership to transfer. The destination takes responsibility and original becomes empty.'),('*owner','Read the integer through the destination that still owns it.'),('original == nullptr','Check the source owner’s empty state without trying to dereference it.')],
 success='std::move permits transfer of exclusive ownership. Copying would try to give the same object two unique owners; creating a new zero-valued object would not transfer the original.',
 task='Complete the supplied `operator+` function for Score. Return a new Score whose points equal a.points + b.points, without changing a or b. The caller reads two point values from 0 to 1000, adds the Scores, and prints the total followed by both original values. Use the named points members; output is already supplied.',
 region_prompts=['Return a new Score containing the sum; keep both input records unchanged.'])

revise(18,r'''
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
''',
 completion=['The call is written through Base&. Which base declaration enables it to select the actual Derived object’s operation?', 'A same-named nonvirtual function is not enough for dispatch through a base reference. The base must declare this as a virtual operation.'],
 reason=['Compare a reference to the original Derived with a new Base object copied from it.', 'The new Base stores only the Base portion. No later call can restore a discarded derived portion.'],
 write=['The constructor has already saved both dimensions. Area counts rows times columns, not the distance around the edges.', 'Return the product of width_ and height_. Keep the supplied const override signature so the call through const Shape& can use it.'],
 arrange=['Create the Derived object before making a reference to it.', 'Bind the general reference to that existing object, then call the virtual operation through the reference.'],
 trace=['Name the actual object type separately from the reference type.', 'For a virtual call through a reference to Derived, use Derived’s body even though the reference is declared Base&.'],
 explain=[('virtual int value() const','The base permits selection according to the actual object when called through a base reference.'),('int value() const override','This is Derived’s replacement body; override checks that its signature matches.'),('const Base& base{derived};','Refer to the existing Derived without copying away its more specific part.'),('base.value()','Select the Derived implementation because this is a virtual call on the actual Derived object.')],
 success='virtual in the base enables dispatch through Base&. Removing it would make this call use Base’s operation even though the original object is Derived.',
 task='Complete Rectangle’s supplied `area() const override` body. Return its stored width_ multiplied by its stored height_. The caller reads two dimensions from 1 to 100, constructs a Rectangle, and prints area through a const Shape reference. The constructor, interface, and output are already complete.',
 region_prompts=['Return the rectangle area from its stored dimensions.'])

revise(19,r'''
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
''',
 completion=['Read the observer’s name literally: it should give back the value already stored in this box.', 'Creating a fresh T{} would return a default value, and adding the member to itself would double it. Neither is an observation of the original value.'],
 reason=['Compare “same source pattern” with “same completed type.” What argument was substituted for T in each case?', 'The different template argument lists are part of the type names, so the two instantiations are not the same type.'],
 write=['The constructor has already stored the two T values. The observer only needs to combine them.', 'Add first_ and second_ directly and return that result. Preserve T so the fractional pair can return a fractional sum.'],
 arrange=['Choose and construct the concrete box before asking its observer for a value.', 'Printing the observed value is the last step. The supplied class definition handles the type pattern and storage.'],
 trace=['Replace T with the concrete type named in the program, then record the value supplied to that box’s constructor.', 'The observer does not modify the member; use the same stored number when predicting the print.'],
 explain=[('template <typename T>','This class is a pattern whose member and result types are chosen by its template argument.'),('explicit Box(T value) : value_{value} {}','Store the constructor argument in the member with the same chosen type.'),('T value() const { return value_; }','Return the stored value without changing it or converting it to a fixed type.'),('Box<double> fraction{2.5};','This is a separate double-valued instantiation; its fraction should survive observation.')],
 success='Returning the existing member preserves exactly what was stored. A default-constructed T or a doubled member would answer a different question.',
 task='Complete the supplied `Pair<T>::sum() const` observer by returning first_ + second_. The caller reads two integers from −1000 to 1000 and also tests a Pair<double> containing 1.25 and 2.5. It prints both sums. Keep the result type T and leave both members unchanged.',
 region_prompts=['Return the sum of the two stored T members without changing them.'])

revise(20,r'''
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
''',
 completion=['Division fails when the divisor is zero, not when the dividend is zero.', 'Try the valid calculation zero divided by three. Rejecting a zero numerator would incorrectly reject that case.'],
 reason=['Think about a local owner whose scope is left when a calculation throws.', 'Stack unwinding performs the cleanup of fully constructed local objects; it does not limit cleanup only to the exception object.'],
 write=['First try to read both required integers. A successful first read alone is not enough.', 'Then look for one extra non-whitespace token. Accept only when the required reads succeeded and that extra read did not.'],
 arrange=['The try block contains the operation that can fail; the matching handler deals with its thrown exception.', 'The output after a successful call belongs on the normal path. The handler’s output belongs only on the failure path.'],
 trace=['Check the denominator before doing any arithmetic. If it is zero, follow the throw into the handler.', 'A throw stops the rest of that try path. Predict only the output statements actually reached.'],
 explain=[('denominator == 0','Check the divisor, because a zero divisor makes division invalid. A zero numerator is allowed.'),('throw std::invalid_argument{"zero"};','Signal the failure with a standard error object whose message is zero; do not compute a quotient on this path.'),('try {','Begin the normal path that may transfer control to a handler if a call throws.'),('catch (const std::exception& error)','Catch and observe a standard exception. Its what() message can explain the failure.')],
 success='Only a zero denominator makes this integer division invalid. Checking the numerator would reject a valid zero result and miss the actual error.',
 choices=[('Their destructors run.','Fully constructed local owners are cleaned up as their scopes are left, so resources do not need a separate manual cleanup path here.'),('Their destructors are skipped, so every thrown exception requires manual deletion.','This overlooks stack unwinding: automatic local owners are specifically useful because their destructors still run.'),('Only the thrown exception object is destroyed; other local owners remain alive forever.','Cleanup follows the exited scopes too. It is not restricted to the exception object.')],
 region_prompts=['Accept exactly two integers with no extra token; print their sum or invalid.'])

# Sharpen a few conceptual distractors that previously asked implausible questions.
MODULES[0]['choices']=[
 ('It starts n at zero.','Empty braces supply the integer’s starting zero. No input operation is needed.'),
 ('It leaves n without a starting value.','This confuses empty braces with leaving initialization out entirely. The braces make the integer start at zero.'),
 ('It waits for the user to enter n.','A declaration creates the variable. Reading a later input is a separate std::cin operation.')]
MODULES[5]['choices']=[
 ('The first comparison produces a bool, and that result is then compared with 10.','C++ does not read this as two comparisons of n. Write both comparisons explicitly and join them with &&.'),
 ('It automatically checks both bounds of n, just as a mathematical chained inequality does.','The mathematical notation is tempting, but C++ evaluates a comparison result before the next comparison.'),
 ('The chain is the same as n <= 10 because its lower bound is discarded.','The lower comparison is evaluated, but its true/false result—not n—is what the second comparison receives.')]
MODULES[6]['choices']=[
 ('A static local name is limited to its block, while its stored value survives later calls.','Scope concerns the name; storage duration concerns how long the object persists.'),
 ('Adding static makes a local name available in every function.','Its value lasts longer, but the declaration still has local scope.'),
 ('Every return resets all local values, including static locals, to their initializer.','That is the useful difference here: an ordinary local is recreated, but a static local is initialized once.')]
MODULES[8]['choices']=[
 ('Input validation must still work when assertions are disabled.','Assertions check developer assumptions and may be absent in a release build. Normal invalid input needs ordinary program logic.'),
 ('An assertion that passed during development must remain active in every release build.','Build settings can disable assertions. Passing an earlier test does not guarantee later input handling.'),
 ('Initializing score to zero means a failed read is already a valid input.','A fallback initial value does not mean the user supplied that value. Check whether the read succeeded before accepting it.')]
MODULES[10]['choices']=[
 ('No; a constexpr function may also be called with runtime values.','constexpr permits constant evaluation when the call and its context support it; it does not require every call to happen during a build.'),
 ('Yes; constexpr forces every call to run before the program starts.','A normal call can receive a value read from input, which is unavailable during compilation.'),
 ('No runtime call is allowed because the compiler only accepts literal arguments.','The function can accept runtime arguments too. A context that specifically requires a constant expression has the extra restriction.')]
MODULES[14]['choices']=[
 ('0','reserve makes space available but does not construct list elements.'),
 ('10','This confuses capacity with size. resize(10), not reserve(10), would create ten elements.'),
 ('The call is an error because an empty vector cannot reserve storage.','Preparing capacity before inserting items is a normal use of reserve, even when the size is zero.')]

# Goals describe the practiced skills, without claiming every optional reading is assessed.
GOALS=[
 ['Read and initialize whole-number values.','Connect arithmetic with one line of output.','Use a small input example to test a calculation.'],
 ['Follow arguments into a function and its return value back to main.','Distinguish a visible declaration from a definition.','Write a different rectangle calculation in a supplied function.'],
 ['Trace assignments without losing an original value.','Choose an input that exposes a faulty swap.','Repair and test a small block of code.'],
 ['Distinguish whole-number and fractional division.','Convert an operand before division.','Calculate and format a two-score average.'],
 ['Read, measure, and query stored text.','Use C++23 string contains.','Distinguish owning a string from viewing someone else’s characters.'],
 ['Combine complete comparisons with AND.','Include endpoints deliberately.','Combine a range and an evenness test.'],
 ['Distinguish a name’s scope from a value’s lifetime.','Trace a static local across calls.','Use a function inside a namespace.'],
 ['Trace a counting loop and running total.','Choose inclusive bounds.','Sum a sequence that may be empty.'],
 ['Separate reading success from allowed values.','Check threshold and range boundaries.','Handle invalid input with a clear result.'],
 ['Predict the type deduced by auto.','Identify where integer division loses a fraction.','Keep a fractional result until output formatting.'],
 ['Use one function template for integers and doubles.','Follow a conditional result choice.','Distinguish permitted compile-time and runtime evaluation.'],
 ['Update a caller’s value through a reference.','Read through a valid pointer.','Explain why an address cannot extend a local object’s lifetime.'],
 ['Create and read named record members.','Use scoped enum values.','Return a translated Point in the correct member order.'],
 ['Connect construction, controlled updates, and observation.','Keep a class rule intact for rejected requests.','Call a const observer on a shared object.'],
 ['Distinguish vector size and capacity.','Read an iterator range and range-based loop.','Count qualifying values, including an empty list.'],
 ['Distinguish a captured copy from its original.','Trace an ordinary lambda call.','Write a recursive calculation with a stopping case.'],
 ['Track exclusive ownership after a unique_ptr move.','Use an operator function for a value record.','Return a new value without mutating either operand.'],
 ['Distinguish a reference’s declared type from its actual object.','Follow a virtual call and explain slicing.','Supply a matching const override.'],
 ['Instantiate a class template with different types.','Read stored members through a const observer.','Return a generic sum without losing fractional information.'],
 ['Follow a thrown error to its handler.','Explain cleanup during stack unwinding.','Validate a complete line of two input fields.']]
for m,goals in zip(MODULES,GOALS):m['objectives']=goals

def example_puzzle(n,blocks,goal,**kw):puzzle(n,MODULES[n-1]['example'],blocks,goal,**kw)

example_puzzle(1,[
 ('    int boxes{4};','Choose the number of boxes before the total can use it.'),
 ('    int perBox{3};','Choose how many items each box holds. This can be prepared before or after boxes.'),
 ('    int total{boxes * perBox};','Once both counts exist, multiply them to get the total.'),
 (r"    std::cout << total << '\n';",'Display the total only after it has been calculated.')],
 'Build a program that counts the items in four boxes with three items in each and prints that total.',groups={0:'starting-counts',1:'starting-counts'})
example_puzzle(2,[
 ('    int width{3};','Supply the rectangle width before passing it to the function.'),
 ('    int height{5};','Supply the rectangle height. The two dimension declarations can be in either order.'),
 (r"    std::cout << rectanglePerimeter(width, height) << '\n';",'Call the visible perimeter definition with both dimensions and print its returned answer.')],
 'Prepare width 3 and height 5, then call rectanglePerimeter and print its answer. The declaration in geometry.hpp and the definition below main are supplied.',groups={0:'dimensions',1:'dimensions'})
example_puzzle(3,[
 ('    int saved{left};','Save the original left value before overwriting it.'),
 ('    left = right;','Move the original right value into left while saved protects the other original.'),
 ('    right = saved;','Finish by recovering the original left value from saved.'),
 (r"    std::cout << left << ' ' << right << '\n';",'Print after the whole swap is complete, so both positions show their final values.')],
 'Swap the supplied left and right values without losing either original, then print the swapped pair.')
example_puzzle(4,[
 ('    int sum{15}, count{4};','Create the two integer inputs that the following division needs.'),
 ('    double average{static_cast<double>(sum) / count};','Convert before division to keep the fractional part.'),
 (r"    std::cout << sum / count << ' ' << average << '\n';",'Compare the integer quotient with the already calculated fractional average.')],
 'Print the integer quotient and fractional quotient for a total of 15 shared among 4 items.')
puzzle(5,r'''
 #include <iostream>
 #include <string>
 int main() {
     const std::string word{"cupcake"};
     bool found{word.contains("cake")};
     std::cout << std::boolalpha << found << '\n';
 }
 ''',[
 ('    const std::string word{"cupcake"};','Create the owning text before searching it.'),
 ('    bool found{word.contains("cake")};','Ask the C++23 contains question and store its true/false answer.'),
 (r"    std::cout << std::boolalpha << found << '\n';",'Display the stored answer as a word, not a numeric flag.')],
 'Create the word cupcake, ask whether it contains cake, and print the Boolean answer as a word.')
example_puzzle(6,[
 ('    int age{16};','Create the input variable before reading into it.'),
 ('    std::cin >> age;','Read the actual test age before calculating eligibility.'),
 ('    bool eligible{age >= 12 && age <= 17};','Require both inclusive age limits after the read succeeds for these integer inputs.'),
 (r"    std::cout << std::boolalpha << eligible << '\n';",'Print the calculated eligibility, with boolalpha making it a word.')],
 'Read an integer age and print true only for ages 12 through 17, including both endpoints.',stdin='16\n')
puzzle(7,r'''
 #include <iostream>
 int nextTicket() {
     static int ticket{0};
     return ++ticket;
 }
 int main() {
     int first{nextTicket()};
     int second{nextTicket()};
     std::cout << first << ' ' << second << '\n';
 }
 ''',[
 ('    int first{nextTicket()};','Issue and retain the first ticket before requesting the second one.'),
 ('    int second{nextTicket()};','The same static counter continues from the first call, giving the next ticket.'),
 (r"    std::cout << first << ' ' << second << '\n';",'Print the first and second results in their issue order.')],
 'Request the first ticket, then the second, and print them in that order. nextTicket and its persistent counter are already supplied.')
example_puzzle(8,[
 ('    int total{0};','Start the sum once, before any loop visit.'),
 ('    for (int i{1}; i <= limit; ++i) {\n        total += i;\n    }','Add every integer from one through the supplied limit. Keep the loop as one block.'),
 (r"    std::cout << total << '\n';",'Display the completed total after the loop finishes.')],
 'Use the supplied limit to add 1 through limit, then print one final total.')
example_puzzle(9,[
 ('    int score{};','Create score before trying to read it.'),
 ('    if (!(std::cin >> score)) {\n        std::cout << "invalid\\n";\n        return 0;\n    }','Reject a failed read and stop before testing the numeric range.'),
 ('    if (score >= 0 && score <= 100) {\n        std::cout << "valid\\n";\n    } else {\n        std::cout << "invalid\\n";\n    }','After successful parsing, choose a result from the allowed inclusive range.')],
 'Read a score, reject a failed read, and then print valid for 0–100 or invalid for other integers.',stdin='75\n')
example_puzzle(10,[
 ('    auto whole{9 / 2};','Create the whole-number quotient. This and the fractional quotient can be calculated in either order.'),
 ('    auto fraction{static_cast<double>(9) / 2};','Create the fractional quotient with a converted operand; it does not depend on whole.'),
 (r"    std::cout << whole << ' ' << fraction << '\n';",'Both quotients must exist before this comparison can be printed.')],
 'Calculate both quotient forms, then print the whole-number result followed by the fractional result.',groups={0:'independent-quotients',1:'independent-quotients'})
puzzle(11,r'''
 #include <iostream>
 template <typename T>
 constexpr T larger(T a, T b) { return a < b ? b : a; }
 int main() {
     int a{3}, b{8};
     auto result{larger(a, b)};
     std::cout << result << '\n';
 }
 ''',[
 ('    int a{3}, b{8};','Prepare the argument values before calling the template.'),
 ('    auto result{larger(a, b)};','Deduce T as int for this call and keep its returned larger value.'),
 (r"    std::cout << result << '\n';",'Display the returned result; the template itself does not print.')],
 'Prepare the pair 3 and 8, call the supplied larger template, and print its returned value.')
puzzle(12,r'''
 #include <iostream>
 int main() {
     int score{10};
     int& alias{score};
     alias += 5;
     std::cout << score << '\n';
 }
 ''',[
 ('    int score{10};','The actual integer must exist before a reference can name it.'),
 ('    int& alias{score};','Bind another name to that same integer; do not create a separate copy.'),
 ('    alias += 5;','Modify the shared integer through its reference.'),
 (r"    std::cout << score << '\n';",'Read the updated object through its original name.')],
 'Create score, bind an alias to it, increase the shared value by five, then print score.')
puzzle(13,r'''
 #include <iostream>
 enum class Status { waiting, ready };
 struct Parcel { int weight{}; Status status{Status::waiting}; };
 int main() {
     Parcel parcel{4, Status::ready};
     parcel.weight += 2;
     if (parcel.status == Status::ready) {
         std::cout << parcel.weight << '\n';
     }
 }
 ''',[
 ('    Parcel parcel{4, Status::ready};','Create both named record members in their declaration order.'),
 ('    parcel.weight += 2;','Update the weight member of the existing record before displaying it.'),
 ('    if (parcel.status == Status::ready) {\n        std::cout << parcel.weight << \'\\n\';\n    }','Check the scoped status value and print the updated weight for a ready parcel.')],
 'Create a ready parcel of weight 4, add 2 to its weight, and print the updated weight only when ready.')
example_puzzle(14,[
 ('    Counter counter{3};','Construct the object and give its member the starting value.'),
 ('    counter.increment();','Use the public update on the object that now exists.'),
 (r"    std::cout << counter.value() << '\n';",'Observe the count after the update rather than printing the original count.')],
 'Create a Counter starting at three, increment it once, and print its new value through the public observer.')
example_puzzle(15,[
 ('    std::vector<int> values{5, 1, 3};','Create the existing elements before describing their range.'),
 ('    std::sort(values.begin(), values.end());','Sort the complete vector before visiting it for output.'),
 (r'''    for (int value : values) {
        std::cout << value << ' ';
    }
    std::cout << '\n';''','Visit the sorted elements and finish their display with a newline.')],
 'Create the three-element vector, sort all of it, then print its elements in increasing order.')
example_puzzle(16,[
 ('    int bonus{3};','The original value must exist before a lambda can capture it.'),
 ('    auto addBonus{[bonus](int value) { return value + bonus; }};','Capture the earlier bonus before the later assignment changes the original.'),
 ('    bonus = 9;','Change only the original variable after the captured copy has been created.'),
 (r"    std::cout << addBonus(4) << '\n';",'Call the lambda and display the sum using its earlier captured copy.')],
 'Capture the original bonus, change the original afterward, and print addBonus(4) using the saved copy.')
example_puzzle(17,[
 ('    auto original{std::make_unique<int>(7)};','Create the integer and give it one exclusive owner.'),
 ('    auto owner{std::move(original)};','Transfer that existing ownership to the destination.'),
 (r"    std::cout << *owner << ' ' << std::boolalpha << (original == nullptr) << '\n';",'Observe the destination value and the source’s empty state after the move.')],
 'Create one owned integer, transfer its unique_ptr, then print the value and whether the source is empty.')
example_puzzle(18,[
 ('    Derived derived;','Construct the actual specific object first.'),
 ('    const Base& base{derived};','Refer to that object through the general interface without making a base-value copy.'),
 (r"    std::cout << base.value() << '\n';",'Make the virtual call through the reference; its actual Derived object selects the body.')],
 'Construct Derived, refer to it through const Base&, and print the virtual value call’s result.')
puzzle(19,r'''
 #include <iostream>
 template <typename T>
 class Box {
     T value_;
 public:
     explicit Box(T value) : value_{value} {}
     T value() const { return value_; }
 };
 int main() {
     Box<int> box{8};
     int observed{box.value()};
     std::cout << observed << '\n';
 }
 ''',[
 ('    Box<int> box{8};','Choose the integer instantiation and construct one box with its stored value.'),
 ('    int observed{box.value()};','Read the existing member through its const observer.'),
 (r"    std::cout << observed << '\n';",'Display the returned value; observation did not change the box.')],
 'Construct an integer Box, read its value into observed, and print that observation.')
puzzle(20,r'''
 #include <iostream>
 #include <stdexcept>
 int checkedDivide(int numerator, int denominator) {
     if (denominator == 0) { throw std::invalid_argument{"zero"}; }
     return numerator / denominator;
 }
 int main() {
     int numerator{12};
     int denominator{0};
     try {
         std::cout << checkedDivide(numerator, denominator) << '\n';
     } catch (const std::exception& error) {
         std::cout << error.what() << '\n';
     }
 }
 ''',[
 ('    int numerator{12};','Prepare the number being divided. It is independent of the divisor declaration.'),
 ('    int denominator{0};','Prepare the zero divisor that will cause the supplied function to throw.'),
 (r'''    try {
        std::cout << checkedDivide(numerator, denominator) << '\n';
    } catch (const std::exception& error) {
        std::cout << error.what() << '\n';
    }''','Run the risky operation with both arguments available and handle the thrown error with its matching catch.')],
 'Prepare 12 and a zero divisor, then use the supplied checkedDivide inside a try/catch so its error message is printed.',groups={0:'arguments',1:'arguments'})

tracing(1,r'''
 #include <iostream>
 int main() {
     int boxes{2};
     int perBox{3};
     int total{boxes * perBox};
     std::cout << total << '\n';
 }
 ''','2',[2,4,7],'The number of boxes changes between versions. Predict the single total printed for the values on your screen.',[
 ('int boxes{2};','Start with two boxes in this walkthrough.',{'boxes':2}),
 ('int perBox{3};','Each box holds three items; the number of boxes is unchanged.',{'perBox':3}),
 ('int total{boxes * perBox};','Two equal groups of three contain six items altogether.',{'total':6}),
 (r"std::cout << total << '\n';",'Print the stored total and then end the line.',{'output':'6'})],
 '6\n',expected=['6\n','12\n','21\n'])
tracing(2,r'''
 #include <iostream>
 int rectanglePerimeter(int width, int height) {
     return 2 * (width + height);
 }
 int main() {
     int width{3};
     int height{5};
     std::cout << rectanglePerimeter(width, height) << '\n';
 }
 ''','3',[3,1,5],'The width changes. Follow the call into the visible perimeter function and predict its returned result on the one output line.',[
 ('int width{3};','Prepare the caller’s width, three.',{'width':3}),
 ('int height{5};','Prepare the caller’s height, five.',{'height':5}),
 ('rectanglePerimeter(width, height)','Supply those two values to the function parameters.',{'parameter width':3,'parameter height':5}),
 ('return 2 * (width + height);','Add three and five, then double that sum. The result returns to main.',{'returned value':16}),
 (r"std::cout << rectanglePerimeter(width, height) << '\n';",'The output expression receives the returned sixteen and prints it once.',{'output':'16'})],
 '16\n',expected=['16\n','12\n','20\n'])
tracing(3,r'''
 #include <iostream>
 int main() {
     int left{2}, right{9};
     int saved{left};
     left = right;
     right = saved;
     std::cout << left << ' ' << right << '\n';
 }
 ''','2',[2,0,-4],'The original left value changes. Predict the two values printed after the complete swap.',[
 ('int left{2}, right{9};','Record both originals before changing either one.',{'left':2,'right':9}),
 ('int saved{left};','Keep the original left in saved.',{'saved':2}),
 ('left = right;','Replace left with nine. saved still protects the old two.',{'left':9}),
 ('right = saved;','Replace right with that preserved two.',{'right':2}),
 (r"std::cout << left << ' ' << right << '\n';",'Print the final left and right separated by a space.',{'output':'9 2'})],
 '9 2\n',expected=['9 2\n','9 0\n','9 -4\n'])
tracing(4,r'''
 #include <iostream>
 int main() {
     int sum{15};
     int count{4};
     int whole{sum / count};
     double average{static_cast<double>(sum) / count};
     std::cout << whole << ' ' << average << '\n';
 }
 ''','15',[15,16,3],'The total changes. Predict the integer quotient followed by the fractional quotient, in that order.',[
 ('int sum{15};','The total for this walkthrough is fifteen.',{'sum':15}),
 ('int count{4};','Share that total among four items.',{'count':4}),
 ('int whole{sum / count};','Two integers produce a whole-number quotient, dropping the fraction.',{'whole':3}),
 ('double average{static_cast<double>(sum) / count};','Convert before dividing to retain the fractional part.',{'average':'3.75'}),
 (r"std::cout << whole << ' ' << average << '\n';",'Print the whole-number result first and the fractional result second.',{'output':'3 3.75'})],
 '3 3.75\n',expected=['3 3.75\n','4 4\n','0 0.75\n'])
tracing(5,r'''
 #include <iostream>
 #include <string>
 int main() {
     const std::string word{"cat"};
     std::cout << word.size() << '\n';
 }
 ''','"cat"',['"cat"','"ice cream"','""'],'The stored text changes. Count its ASCII characters, including any spaces, and predict the printed length.',[
 ('const std::string word{"cat"};','Store the three letters c, a, and t. The quote marks delimit the text; they are not stored characters.',{'word':'cat'}),
 ('word.size()','Ask how many characters are stored. No newline was stored in this literal.',{'length':3}),
 (r"std::cout << word.size() << '\n';",'Print the length, then add an output newline.',{'output':'3'})],
 '3\n',expected=['3\n','9\n','0\n'])
tracing(6,r'''
 #include <iostream>
 int main() {
     int age{14};
     bool eligible{age >= 12 && age <= 17};
     std::cout << std::boolalpha << eligible << '\n';
 }
 ''','14',[14,11,18],'The age changes. Check both inclusive bounds before predicting the true/false word.',[
 ('int age{14};','Begin with age fourteen in this walkthrough.',{'age':14}),
 ('age >= 12 && age <= 17','Fourteen meets the lower bound and the upper bound, so both conditions hold.',{'lower bound':'true','upper bound':'true','eligible':'true'}),
 (r"std::cout << std::boolalpha << eligible << '\n';",'boolalpha displays the stored answer as the word true.',{'output':'true'})],
 'true\n',expected=['true\n','false\n','false\n'])
tracing(7,r'''
 #include <iostream>
 int nextTicket() {
     static int ticket{0};
     return ++ticket;
 }
 int main() {
     int first{nextTicket()};
     int second{nextTicket()};
     std::cout << first << ' ' << second << '\n';
 }
 ''','0',[0,5,9],'The static counter’s starting value changes. Predict the first and second tickets, remembering the counter between calls.',[
 ('static int ticket{0};','On the first call only, initialize the remembered counter to zero.',{'ticket':0}),
 ('return ++ticket;','The first call increases the counter before returning it.',{'ticket':1,'returned value':1}),
 ('int first{nextTicket()};','Keep that returned one as first.',{'first':1}),
 ('return ++ticket;','The next call reuses the counter, increasing one to two instead of initializing again.',{'ticket':2,'returned value':2}),
 ('int second{nextTicket()};','Keep the second returned ticket separately.',{'second':2}),
 (r"std::cout << first << ' ' << second << '\n';",'Display the issue order: first, then second.',{'output':'1 2'})],
 '1 2\n',expected=['1 2\n','6 7\n','10 11\n'],context='static int ticket{0};')
tracing(8,r'''
 #include <iostream>
 int main() {
     int limit{3};
     int total{0};
     for (int i{1}; i <= limit; ++i) {
         total += i;
     }
     std::cout << total << '\n';
 }
 ''','3',[3,0,5],'The limit changes. Add the values reached by the loop, including the limit when it is visited.',[
 ('int limit{3};','The walkthrough includes one through three.',{'limit':3}),
 ('int total{0};','Before any loop visits, the running total is zero.',{'total':0}),
 ('for (int i{1}; i <= limit; ++i) {','Start i at one. One passes the inclusive limit check.',{'i':1}),
 ('total += i;','The first contribution changes zero to one.',{'total':1}),
 ('for (int i{1}; i <= limit; ++i) {','Advance i to two. It still passes the condition.',{'i':2}),
 ('total += i;','Add two to the previous one.',{'total':3}),
 ('for (int i{1}; i <= limit; ++i) {','Advance i to three. Equality is allowed by <=.',{'i':3}),
 ('total += i;','Add three to the previous three.',{'total':6}),
 ('for (int i{1}; i <= limit; ++i) {','The next candidate is four, which fails the test. The body does not run again.',{'i':4}),
 (r"std::cout << total << '\n';",'The loop has ended; its local i is no longer in scope. Print the completed total.',{'i':'out of scope','output':'6'})],
 '6\n',expected=['6\n','0\n','15\n'])
tracing(9,r'''
 #include <iostream>
 int main() {
     int score{60};
     if (score < 0 || score > 100) {
         std::cout << "invalid\n";
     } else if (score >= 60) {
         std::cout << "pass\n";
     } else {
         std::cout << "retry\n";
     }
 }
 ''','60',[60,59,101],'The score changes. Choose the one branch reached after range validation, then predict its printed word.',[
 ('int score{60};','The fixed walkthrough starts at the first passing score.',{'score':60}),
 ('if (score < 0 || score > 100) {','Sixty is neither below zero nor above one hundred, so the invalid branch is skipped.',{'out of range':'false'}),
 ('} else if (score >= 60) {','The valid score meets the pass threshold, including equality.',{'reaches pass threshold':'true'}),
 ('std::cout << "pass\\n";','Print the passing word. The retry branch is not also executed.',{'output':'pass'})],
 'pass\n',expected=['pass\n','retry\n','invalid\n'],context='int score{60};')
tracing(10,r'''
 #include <iostream>
 int main() {
     int total{9};
     int count{2};
     auto average{static_cast<double>(total) / count};
     std::cout << average << '\n';
 }
 ''','9',[9,8,1],'The total changes. Follow the operand conversion and predict the quotient printed with the stream’s default formatting.',[
 ('int total{9};','The walkthrough total is nine, stored as an integer.',{'total':9}),
 ('int count{2};','The count is two.',{'count':2}),
 ('auto average{static_cast<double>(total) / count};','A converted operand gives fractional division; auto follows that double result.',{'average':'4.5','deduced type':'double'}),
 (r"std::cout << average << '\n';",'Print four and a half. This trace does not request a fixed number of decimal places.',{'output':'4.5'})],
 '4.5\n',expected=['4.5\n','4\n','0.5\n'])

tracing(11,r'''
 #include <iostream>
 template <typename T>
 constexpr T larger(T a, T b) { return a < b ? b : a; }
 int main() {
     int a{3};
     int b{8};
     std::cout << larger(a, b) << '\n';
 }
 ''','3',[3,12,8],'The first argument changes. Choose the larger returned value, including the equal-values case.',[
 ('int a{3};','Prepare the first argument as an int.',{'a':3}),
 ('int b{8};','Prepare the second int argument; T will be int for this call.',{'b':8,'chosen T':'int'}),
 ('return a < b ? b : a;','Three is less than eight, so choose b from the true branch.',{'comparison':'true','returned value':8}),
 (r"std::cout << larger(a, b) << '\n';",'The caller prints the returned larger value once.',{'output':'8'})],
 '8\n',expected=['8\n','12\n','8\n'])
tracing(12,r'''
 #include <iostream>
 int main() {
     int score{10};
     int& alias{score};
     alias += 5;
     std::cout << score << '\n';
 }
 ''','10',[10,0,-3],'The original score changes. Follow the update through its alias and predict the value printed through the original name.',[
 ('int score{10};','Create one integer holding ten.',{'score':10}),
 ('int& alias{score};','Bind an alias to that same object, rather than copying ten into another integer.',{'alias':'refers to score'}),
 ('alias += 5;','Update the one shared integer through its alias.',{'score':15}),
 (r"std::cout << score << '\n';",'The original name reads the updated shared value.',{'output':'15'})],
 '15\n',expected=['15\n','5\n','2\n'])
tracing(13,r'''
 #include <iostream>
 struct Point { int x{}; int y{}; };
 int main() {
     Point start{4, 2};
     Point moved{start.x + 3, start.y - 1};
     std::cout << moved.x << ' ' << moved.y << '\n';
 }
 ''','4',[4,0,-2],'The initial x coordinate changes. Predict the moved x and moved y, in declaration order.',[
 ('Point start{4, 2};','Match the initializers to the named members: x first, y second.',{'start.x':4,'start.y':2}),
 ('Point moved{start.x + 3, start.y - 1};','Create a new point: add three horizontally and subtract one vertically. start is unchanged.',{'moved.x':7,'moved.y':1}),
 (r"std::cout << moved.x << ' ' << moved.y << '\n';",'Print the new point’s members in x-then-y order.',{'output':'7 1'})],
 '7 1\n',expected=['7 1\n','3 1\n','1 1\n'])
tracing(14,r'''
 #include <iostream>
 class Counter {
     int value_{};
 public:
     explicit Counter(int start) : value_{start} {}
     void add(int amount) { if (amount > 0) { value_ += amount; } }
     int value() const { return value_; }
 };
 int main() {
     Counter counter{3};
     counter.add(2);
     std::cout << counter.value() << '\n';
 }
 ''','2',[2,0,-2],'The requested addition changes. Apply the method’s positive-only rule before predicting the observer’s result.',[
 ('Counter counter{3};','The constructor stores the initial count of three.',{'stored count':3}),
 ('counter.add(2);','The request is positive, so the method accepts it and adds two.',{'requested amount':2,'stored count':5}),
 (r"std::cout << counter.value() << '\n';",'The const observer returns the final count without changing it.',{'output':'5'})],
 '5\n',expected=['5\n','3\n','3\n'],context='counter.add(2);')
tracing(15,r'''
 #include <iostream>
 #include <vector>
 int main() {
     std::vector<int> values{2, -1, 0};
     int count{0};
     for (int value : values) {
         if (value > 0) { ++count; }
     }
     std::cout << count << '\n';
 }
 ''','2',[2,-2,0],'The first vector element changes. Count strictly positive elements; do not add their values or count zero.',[
 ('std::vector<int> values{2, -1, 0};','Create the three existing elements in visit order.',{'values':'2, -1, 0'}),
 ('int count{0};','No qualifying element has been seen yet.',{'count':0}),
 ('for (int value : values) {','Visit the first element, two.',{'value':2}),
 ('if (value > 0) { ++count; }','Two is positive, so count one qualifying element.',{'count':1}),
 ('for (int value : values) {','Visit the next element, negative one.',{'value':-1}),
 ('if (value > 0) { ++count; }','A negative value does not qualify; leave count unchanged.',{'count':1}),
 ('for (int value : values) {','Visit the final element, zero.',{'value':0}),
 ('if (value > 0) { ++count; }','The comparison is strict: zero is not positive.',{'count':1}),
 (r"std::cout << count << '\n';",'After all visits, print the number of qualifying elements.',{'value':'out of scope','output':'1'})],
 '1\n',expected=['1\n','0\n','0\n'])
tracing(16,r'''
 #include <iostream>
 int main() {
     int bonus{3};
     auto addBonus{[bonus](int value) { return value + bonus; }};
     bonus = 9;
     std::cout << addBonus(4) << '\n';
 }
 ''','3',[3,0,7],'The bonus at capture time changes. Predict the later lambda call using its saved copy, not the changed original.',[
 ('int bonus{3};','The original starts at three.',{'original bonus':3}),
 ('auto addBonus{[bonus](int value) { return value + bonus; }};','Create the lambda now and save a copy of three.',{'captured bonus':3}),
 ('bonus = 9;','Only the original variable changes to nine.',{'original bonus':9}),
 ('addBonus(4)','The call argument four is added to the saved three.',{'call value':4,'returned value':7}),
 (r"std::cout << addBonus(4) << '\n';",'Print the returned seven. The captured copy was not changed by the assignment.',{'output':'7'})],
 '7\n',expected=['7\n','4\n','11\n'])
tracing(17,r'''
 #include <iostream>
 #include <memory>
 #include <utility>
 int main() {
     auto original{std::make_unique<int>(7)};
     auto owner{std::move(original)};
     std::cout << *owner << ' ' << std::boolalpha << (original == nullptr) << '\n';
 }
 ''','7',[7,0,-2],'The owned integer changes. Predict its value after ownership transfer and the source-empty Boolean result.',[
 ('auto original{std::make_unique<int>(7)};','Create an integer holding seven. original is its only owner.',{'owned integer':7,'original':'owns the integer'}),
 ('auto owner{std::move(original)};','Transfer responsibility without changing or deleting that integer.',{'owner':'owns the integer','original':'empty'}),
 (r"std::cout << *owner << ' ' << std::boolalpha << (original == nullptr) << '\n';",'Read the integer through owner and separately report that original is empty.',{'output':'7 true'})],
 '7 true\n',expected=['7 true\n','0 true\n','-2 true\n'])
tracing(18,r'''
 #include <iostream>
 struct Base {
     virtual int value() const { return 1; }
     virtual ~Base() = default;
 };
 struct Derived : Base {
     int value() const override { return 2; }
 };
 int main() {
     Derived derived;
     const Base& base{derived};
     std::cout << base.value() << '\n';
 }
 ''','2',[2,4,6],'The value returned by Derived changes. Predict the virtual call through Base& without treating that reference as a sliced copy.',[
 ('Derived derived;','Construct a complete Derived object.',{'actual object':'Derived'}),
 ('const Base& base{derived};','The reference’s interface is Base, but its object remains the same Derived.',{'reference type':'const Base&','actual object':'Derived'}),
 ('int value() const override { return 2; }','The virtual call chooses this derived body and returns two.',{'selected body':'Derived::value','returned value':2}),
 (r"std::cout << base.value() << '\n';",'Print the result of that selected body.',{'output':'2'})],
 '2\n',expected=['2\n','4\n','6\n'],context='int value() const override { return 2; }')
tracing(19,r'''
 #include <iostream>
 template <typename T>
 class Box {
     T value_;
 public:
     explicit Box(T value) : value_{value} {}
     T value() const { return value_; }
 };
 int main() {
     Box<int> box{8};
     std::cout << box.value() << '\n';
 }
 ''','8',[8,0,-3],'The constructor argument changes. Follow storage in Box<int> and its unchanged value returned by the observer.',[
 ('Box<int> box{8};','Choose int for T and construct this object with eight.',{'chosen T':'int','stored member':8}),
 ('T value() const { return value_; }','The observer returns the stored integer. It neither changes nor doubles it.',{'returned value':8}),
 (r"std::cout << box.value() << '\n';",'Print the returned stored value.',{'output':'8'})],
 '8\n',expected=['8\n','0\n','-3\n'])
tracing(20,r'''
 #include <iostream>
 #include <stdexcept>
 int checkedDivide(int numerator, int denominator) {
     if (denominator == 0) { throw std::invalid_argument{"zero"}; }
     return numerator / denominator;
 }
 int main() {
     int denominator{0};
     try {
         std::cout << checkedDivide(12, denominator) << '\n';
     } catch (const std::exception& error) {
         std::cout << error.what() << '\n';
     }
 }
 ''','0',[0,3,4],'The denominator changes. Decide whether the function returns normally or throws, then predict the one printed line.',[
 ('int denominator{0};','Use a zero divisor for this fixed walkthrough.',{'denominator':0}),
 ('if (denominator == 0) { throw std::invalid_argument{"zero"}; }','The guard detects invalid division and throws instead of calculating a quotient.',{'path':'throw','message':'zero'}),
 ('} catch (const std::exception& error) {','Control reaches the handler; it does not continue with a normal quotient in try.',{'path':'handler'}),
 (r"std::cout << error.what() << '\n';",'Print the exception message on the error path.',{'output':'zero'})],
 'zero\n',expected=['zero\n','4\n','3\n'],context='int denominator{0};')

# Use the same carefully described C++23 input bounds in puzzles as in the parent examples.
for n in (6,9):MODULES[n-1]['puzzle']['cases']=MODULES[n-1]['completion_cases']

CAPSTONES[0]['lesson']=r'''
### A small inventory with one clear rule
An inventory stores a nonnegative number of items. Its class already has a constructor and a stock observer. You write two public actions. Each action first decides whether a request is allowed, then either changes the stock once or rejects the request without changing anything.

`add(amount)` accepts only a positive amount. `take(amount)` also requires that the stock can cover the full amount. For both actions, return true when accepted and false when rejected. This return value is separate from the stored stock: main prints both the decision and the new stock after each command.

### Read the supplied caller
Input begins with initial stock and the number of commands. Each later command is add or take followed by its amount. The loop reads one command at a time. Its conditional expression chooses the matching method. The output uses the returned bool to select ok or rejected, then reads the current stock through the observer. You do not need to change this caller.

### Work in two passes
Complete add first and test a positive, zero, and negative amount. Then complete take and test a small permitted withdrawal, an exact-stock withdrawal, an overdraft, and a zero/negative request. Keep your rejection checks before the update so a failed request cannot change the state.

The two highlighted editor regions are independent method bodies. The read-only surrounding code supplies the names and input/output. In a no-commands case no transaction result is printed; an empty output is correct.
'''.strip()
CAPSTONES[0]['hints']=['Separate the decision from the update. Reject any invalid amount before touching stock_.',
 'For take, ask both “is it positive?” and “is there enough stock?” Exact-stock withdrawal is allowed.',
 'After an accepted update, return true. A rejected request must return false with stock_ exactly as it was.']
CAPSTONES[0]['region_prompts']=['Accept a positive add, update stock_, and return whether it succeeded.', 'Accept a positive take that stock_ can cover; update only when accepted.']
CAPSTONES[1]['lesson']=r'''
### Turn complete text records into a useful report
Each record is one name and one score. Record is a supplied struct with those two named members. The input starts with a line count, followed by that many complete record lines. Names are single words. main already reads the line count, discards the newline left by that numeric read, and obtains each following line with getline. You do not need a file on disk.

### First marked region: parse one line
Build an istringstream from the supplied line. Read into a temporary Record named candidate so a failed parse cannot partly change the caller’s result. Require a name and an integer score, reject scores outside 0–100, and reject an extra non-whitespace token. Only after all checks succeed should you assign result and return true. Otherwise return false; main prints invalid and stops.

### Second marked region: summarize valid records
printReport receives a const reference to the vector that main has built. Count is its size. Add all scores and divide by the count using a double calculation; for an empty vector use 0.0 instead of dividing by zero. fixed and setprecision(1) give the requested one-decimal display.

Use a pointer named best to refer to a record already in that vector. Start it at nullptr. As you visit each const Record&, replace best only when no best exists yet or the current score is strictly higher. A strict comparison preserves the first record in a tie. Because the vector is not changed while reporting, these references stay valid.

### Explain the edge cases before coding
For no records, print count 0, average 0.0, and best none on separate lines. For a tie, keep the first highest-scoring name. A readable score followed by an extra character is not a complete valid record. The test examples below connect each of these rules with concrete input and output. Edit the two marked regions; the surrounding input loop and output contract are supplied.
'''.strip()
CAPSTONES[1]['hints']=['Keep parsing and reporting separate. Validate into a temporary record before changing result.',
 'Two successful fields are not enough: a range violation or one leftover token must reject the line.',
 'In the report, handle the empty vector before division and update best only for a strictly larger score. That protects zero records and first-in-order ties.']
CAPSTONES[1]['region_prompts']=['Parse and validate one full record; assign result only on success.', 'Print count, fractional average, and the first highest-scoring record.']

WRONG_FEEDBACK=[
 ['Adding four and three counts the two labels once each. The goal is four equal groups, each containing three items.', 'Division asks how many groups fit into something; it does not count all items in the supplied groups.'],
 ['This calculates area, the inside of the rectangle. The distance around it includes two widths and two heights.', 'This counts only one width and one height. The opposite two sides are still part of the boundary.'],
 ['left already contains the original right value at this point. Reading it again cannot recover the old left; saved is what preserves that original.', 'This changes saved, not right. The final position would still be waiting for the original left value.'],
 ['Without a double operand, both inputs to division stay integers. Their fractional remainder is dropped before average receives anything.', 'sum is already an int. Converting it to the same type does not make the division fractional.'],
 ['This checks only the beginning. cupcake starts with cup, but cake appears later and should still be found.', 'This asks whether the text has no characters. It does not ask whether the letters cake occur inside it.'],
 ['OR needs only one side. An age below twelve still meets the upper bound, and an age above seventeen still meets the lower bound, so neither is rejected.', 'Strict comparisons leave out twelve and seventeen, even though the requested group includes both endpoints.'],
 ['An ordinary local is initialized again on each call. The two calls would each begin at zero instead of sharing the remembered count.', 'const prevents changing this integer after initialization. The next line needs to increase it, so the declaration would contradict that action.'],
 ['Using < instead of <= stops before the final allowed value can be added. Try a limit of one to see the missing visit.', 'Starting at one and asking whether it equals the supplied limit usually fails immediately. A loop condition should accept the whole intended sequence.'],
 ['The open comparisons reject zero and one hundred. These are explicitly valid endpoints, so both comparisons need to permit equality.', 'OR treats either bound as sufficient. A score above one hundred still meets the lower bound and would incorrectly be accepted.'],
 ['The division inside the cast happens first with two integers. Casting that finished quotient cannot restore its discarded fraction.', 'The two literals are integers, so this keeps whole-number division. auto only follows the result; it does not change the arithmetic.'],
 ['These result branches select the smaller value. Use the same comparison with the opposite result positions to implement the requested larger value.', 'Adding the arguments combines them into a different number. This function must choose and return one of the existing arguments.'],
 ['A value parameter would be a separate copy. Updating that copy would leave the caller’s original score unchanged.', 'A const reference permits reading the caller’s score but prohibits this update. The function is specifically meant to change that score.'],
 ['The record was explicitly initialized as ready. Checking waiting chooses the opposite state, so the intended output path is skipped.', 'Weight and readiness are independent facts in the record. This compares a weight with zero rather than checking its status.'],
 ['Resetting to zero discards the count that was already stored. An increment should build on that value.', 'This moves one step downward, whereas increment means one step upward from the existing value.'],
 ['A range with the same beginning and ending is empty. Sorting no elements leaves the original unsorted vector unchanged.', 'That endpoint includes only the first element. A one-element range is already sorted, but the other values remain outside the work.'],
 ['A reference capture would keep referring to the original bonus. The later assignment to nine would then affect the call, unlike the saved-copy behavior requested.', 'With an empty capture list, the body cannot use this surrounding local bonus. The function needs to retain the value it depends on.'],
 ['unique_ptr cannot be copied into another unique owner. The code needs an explicit ownership transfer, not two separate objects both claiming exclusive ownership.', 'This creates a different integer containing zero. The original would still own its seven, so no ownership was transferred.'],
 ['Without virtual in Base, the call through Base& would select the base operation. The Derived override in this program would also no longer match a virtual operation.', 'A static member belongs to the class rather than an individual object, so it cannot be the virtual object operation being replaced here.'],
 ['T{} creates a fresh default value, such as zero for int. It forgets the value that the constructor stored in this box.', 'This doubles the member rather than observing it. Reading value() should not silently apply a second calculation.'],
 ['This reverses the guard: it rejects usable nonzero divisors and allows the invalid zero divisor to reach division.', 'A zero numerator is valid and gives a zero result for a nonzero divisor. It is the denominator that must not be zero.']]
for m,feedback in zip(MODULES,WRONG_FEEDBACK):
    m['wrong']=[(choice[0],explanation) for choice,explanation in zip(m['wrong'],feedback)]

TASK_TEXT={
 1:'The supplied program reads one whole number n from −1000 to 1000. In the marked line, print its square: n multiplied by itself. Finish the output line with a newline. The reading code is already complete, so you do not need an input prompt.',
 3:'The supplied code reads two whole numbers a and b, each from −1000 to 1000. In the marked block, swap their values using a temporary integer. The supplied output line then prints a followed by b. Preserve both original values; do not change the input or output lines.',
 4:'The supplied code reads two integer scores a and b from 0 to 100. In the marked declaration, calculate their arithmetic mean as a double. Keep a possible half point. The output line already formats mean with exactly one decimal place; leave that formatting in place.',
 5:'Read the complete input line into the supplied std::string text using std::getline. Then print its character count and a newline. Spaces count; the line-ending newline does not. Inputs have at most 200 ASCII characters, and an empty line is allowed.',
 6:'The supplied code reads a whole number n from −100 to 100. Set accepted to true only when n is even and lies between 10 and 20, including both endpoints. Otherwise accepted should be false. The output line already displays the Boolean word.',
 8:'The supplied code reads a limit n from 0 to 1000. In the marked block, use a loop to calculate total: the sum of the positive even numbers no larger than n. For n = 7, the contributions are 2, 4, and 6. The existing output line prints total once after your block.',
 9:'Write the marked decision block to read and classify one score. Print pass for an integer from 60 through 100, retry for an integer from 0 through 59, and invalid for a failed read or an integer outside 0–100. Input is one integer token or one nonnumeric word. Print exactly one result line.',
 10:'The supplied code reads total (0–10000) and count (1–100) as integers. Create average with auto using fractional division, so a half or other fraction is not lost. The supplied output line prints average to two decimal places; do not add another output statement.',
 13:'Complete translated(Point p, int dx, int dy) by returning a new Point with x equal to p.x + dx and y equal to p.y + dy. Input contains x, y, dx, and dy, each from −100 to 100. The supplied caller reads these values and prints the returned x and y. Keep the two directions separate.',
 14:'Complete the marked Counter::add body. Add amount to the stored value_ only when amount is positive; ignore zero and negative requests. Input is a starting count from 0 to 1000 and an amount from −1000 to 1000. The caller constructs the object, requests the update, and prints through the const observer.',
 20:'The supplied code reads one line and creates an istringstream named input. In the marked block, accept exactly two integers with no extra non-whitespace token. Print their sum when valid, or invalid otherwise. Integer values lie between −1000 and 1000. Missing fields, words in place of a required integer, and trailing tokens should be rejected; surrounding whitespace is allowed.'}
for n,text in TASK_TEXT.items():MODULES[n-1]['task']=text

MORE_CASES={
 1:[('Largest magnitude','-1000\n','1000000\n')],
 4:[('Odd total near the upper bound','100 1\n','50.5\n')],
 5:[('Spaces are stored characters','   \n','3\n')],
 6:[('Just below the interval','9\n','false\n')],
 7:[('Upper input bound','1000\n','60000\n')],
 8:[('First even contribution','2\n','2\n')],
 9:[('Negative score','-1\n','invalid\n')],
 10:[('Single item','9 1\n','9.00\n')],
 12:[('Largest allowed positive input','1000\n','1000\n')],
 14:[('Largest allowed positive addition','0 1000\n','1000\n')],
 15:[('Every element qualifies','4\n1 2 3 4\n','4\n')],
 17:[('Large operands stay unchanged','1000 1000\n','2000 1000 1000\n')],
 18:[('Both dimensions at the upper bound','100 100\n','10000\n')],
 20:[('Empty line','\n','invalid\n'),('Two negative values','-3 -7\n','-10\n')]}
for n,cases in MORE_CASES.items():MODULES[n-1]['cases'].extend(cases)
CAPSTONES[1]['cases'].extend([
 ('Zero scores still have a best record','2\nAda 0\nGrace 0\n','count 2\naverage 0.0\nbest Ada 0\n'),
 ('Whitespace around valid fields','1\n  Ada 80   \n','count 1\naverage 80.0\nbest Ada 80\n')])

CASE_PURPOSES=[
 ['A positive input checks the basic multiplication.','Zero checks that the result is calculated rather than replaced with a fixed positive answer.','A negative input checks that both factors come from the same signed input.','The largest permitted magnitude checks the complete stated input range.'],
 ['Different dimensions distinguish area from adding side lengths.','A square still uses multiplication, not a special-case formula.','A dimension of one should leave the other as the area.','Larger dimensions help reject a hard-coded answer based on a small example.'],
 ['Different inputs show whether both original values survived.','Equal inputs should still be accepted, even though they cannot expose every swap bug.','A negative value checks that swapping preserves signs as well as positions.'],
 ['An odd total needs a half point, exposing integer division.','Two zero scores check the additive starting boundary.','The score endpoints still have a valid fractional calculation.','An odd total near the upper score bound must keep its half point.'],
 ['A space inside a name must be read and counted.','An empty line is a real input with zero characters.','Punctuation inside an ASCII word counts as characters too.','A whitespace-only line must not be trimmed before measuring.'],
 ['The lower endpoint is allowed when it is even.','The upper endpoint is allowed when it is even.','A value inside the range still fails when odd.','An even number is rejected when above the range.','A negative even number still fails the lower bound.','A value just below the lower endpoint must be rejected.'],
 ['One hour establishes the conversion factor.','Zero hours should convert to zero minutes.','A longer duration must scale using the same rule.','The upper permitted input still uses the same conversion.'],
 ['An even limit includes the limit as a contribution.','An odd limit stops at the preceding even number.','Zero allows no positive even contribution.','A limit of one also allows no positive even contribution.','The upper input bound checks that the entire loop range is included.','The first positive even value should contribute exactly once.'],
 ['Sixty is the first passing score, not a retry.','Fifty-nine is the neighboring retry boundary.','One hundred remains a valid passing score.','A readable integer above the range is still invalid.','A nonnumeric word must not silently become the initialized zero.','Zero is the first valid retry score.','A negative integer is outside the valid score range.'],
 ['A half must survive until two-decimal output formatting.','A non-terminating decimal is rounded by the supplied formatting.','A zero total remains a valid average with positive count.','A count of one should leave the numeric total unchanged before formatting.'],
 ['An increasing pair checks one comparison branch and the fractional template instantiation.','A reversed signed pair checks the other branch.','Equal arguments should return their common value.'],
 ['A negative input must be changed to zero.','Zero is already valid and should remain unchanged.','A positive input must not be reset.','A larger positive input should also remain exactly as supplied.'],
 ['Both directions move independently with positive offsets.','Signed movement must affect only its matching coordinate.','Zero movement should return the original coordinates.'],
 ['A positive request increases the stored count once.','A rejected negative request must preserve the old value.','A zero request should not introduce any change.','A large accepted request still follows the same guarded update.'],
 ['The count must ignore negatives and zero while including both positives.','An empty vector has no qualifying elements and needs no indexing.','An all-negative vector should not produce a positive count.','A one-element positive vector should count that element exactly once.','Every positive element contributes one, regardless of its numeric value.'],
 ['Zero is the direct stopping case; no recursive call is needed.','One reaches the stopping case after one smaller request.','Several levels check the return path as well as descent.','The upper input bound checks progress and the full resulting sum.'],
 ['The total is new, while both original operands must retain their values.','Two zero values remain valid value objects.','Unequal operands help catch a function that accidentally reuses only one member.','Large values must be added without mutating either original.'],
 ['Different dimensions distinguish area from perimeter.','A square still uses the stored dimensions through the same virtual interface.','A thin rectangle checks that neither dimension is ignored.','The upper dimensions check the complete permitted product.'],
 ['The integer sum and the double sum must both use the same template pattern.','Signed integer operands must keep their sign while the double result keeps its fraction.','A zero integer sum must not affect the independent fractional pair.'],
 ['Exactly two readable integer fields are a valid record.','Surrounding whitespace is allowed and a negative value still parses.','One field is not a complete two-field record.','A third integer is an unwanted extra token.','A word in a required integer position must be rejected.','A readable integer prefix followed by letters is not a complete clean record.','An empty line contains neither required field.','Two signed integers still use ordinary addition.']]
for m,purposes in zip(MODULES,CASE_PURPOSES):
    assert len(m['cases'])==len(purposes),(m['slug'],len(m['cases']),len(purposes))
    m['case_purposes']=purposes
CAPSTONES[0]['case_purposes']=['A transaction sequence checks accepted changes, overdraft rejection, and an exact-stock take.', 'Zero and negative amounts must be rejected without changing the count.', 'An empty inventory can accept stock later and then permit an exact take.', 'With no commands, no transaction result lines should be printed.']
CAPSTONES[1]['case_purposes']=['The first highest-scoring name should survive a tie.', 'An empty report must avoid division by zero and use best none.', 'Both score endpoints are valid and should affect the average.', 'An extra token makes the complete record invalid.', 'A score above one hundred is invalid even if it parses.', 'A missing score must reject the line.', 'A leftover letter after a numeric prefix must reject the line.', 'A negative score is outside the range.', 'The average needs its fractional half.', 'Zero scores are valid; the first zero can still be the best record.', 'Whitespace around complete fields is allowed.']

QUESTION_REVISIONS={
 2:[('It gives 8 back to the caller and ends this function call.','The caller can use that returned number in an expression, including a later output statement.'),('It prints 8 on the screen immediately.','Returning and printing are separate actions. A std::cout operation would be needed to display the returned number.'),('It ends every waiting function call, even if this is not main.','A return leaves this call and resumes its caller; it does not end the entire chain of callers.')],
 3:[('Two distinct values, such as 2 and 9.','The displayed result can show whether both different originals survived in opposite positions.'),('Two equal values, such as 5 and 5.','A broken swap that copies one side twice can still display the expected pair when both originals are equal.'),('Every pair is equally useful for exposing a lost original.','Equal inputs can hide this bug. Choose distinguishable values when testing whether both originals were preserved.')],
 4:[('3.0','The integer operands divide first, producing three; that result then becomes a double.'),('3.5','This assumes the destination type changes an earlier operation. Both operands were still integers when division happened.'),('The declaration is rejected because an integer result can never initialize a double.','The constant integer result three can be represented exactly as a double, so this declaration is allowed.')],
 5:[('It must not outlive the characters it views.','The view borrows access. It cannot safely use characters after the object storing those characters is gone.'),('It always owns a separate copy of the text.','A view keeps access information rather than copying all characters. std::string supplies ownership of its stored text.'),('Creating a view keeps every temporary string alive for as long as needed.','Borrowing a view does not extend a temporary string’s lifetime. The original storage still needs to remain alive.')],
 8:[('Three times, with i equal to 0, 1, and 2.','The body runs for those three values. After the update reaches three, the next condition is false.'),('Four times, with i equal to 0 through 3.','This counts the upper endpoint, but the strict less-than condition does not permit i equal to three.'),('Two times, with i equal to 1 and 2.','This forgets the declared starting zero. The condition is checked before the first body, and zero passes it.')],
 10:[('int','The initializer is the whole-number literal six, whose type here is int. That fixes count’s type.'),('double','auto follows the initializer’s actual type, not a possible later use with fractional numbers.'),('A flexible type that can later become double.','C++ deduces one fixed type at this declaration. auto does not make a variable dynamically change its type later.')],
 12:[('The local integer’s lifetime ends when its function returns.','The copied address does not keep an object alive. Using it afterward would access an object whose lifetime has ended.'),('Pointers are unable to store local addresses at all.','A pointer can hold a local address while that object is alive. The issue is keeping that address after the object dies.'),('Returning the pointer automatically makes the local integer live forever.','Returning an address transfers information about a location, not ownership or an extension of the local object’s lifetime.')],
 13:[('Status::ready','Use the scope separator to name the ready value belonging to the enum type Status.'),('Status.ready','Dot selects a member of an object. Status is a type scope, so this is the wrong kind of selection.'),('ready()','The parentheses would make a function call. Here ready is a named value, not a function to run.')],
 14:[('So public operations can preserve the class’s rules for valid state.','Outside callers request changes through methods that can check them before changing the stored count.'),('So even Counter’s own methods are unable to change the stored value.','Private restricts outside access; the class’s own methods still have the access needed to enforce their rules.'),('Because private means the stored value is automatically const.','Access control and constness are separate ideas. A private member can still change through a permitted class operation.')],
 17:[('The destination unique_ptr owns the original object.','Ownership transfers to the destination. For unique_ptr the moved-from source becomes empty, so only one owner remains.'),('Both pointers independently own the same original object.','That would contradict unique ownership. A move changes which object is responsible rather than duplicating responsibility.'),('Neither owns it because transferring ownership immediately deletes the integer.','The integer stays alive during this transfer. The destination takes responsibility for releasing it later.')],
 18:[('Only the Base portion is copied into the new Base object.','This is slicing. The new object really is a Base, rather than a reference to the original complete Derived.'),('The declared Base variable automatically becomes a Derived variable.','The new variable’s type stays Base. Copying does not change that declared type or add a derived portion.'),('The Base variable is just another view of the original Derived object.','That describes a reference more closely. A by-value initialization creates a separate Base object and loses the derived portion.')],
 19:[('No; they are distinct types made from the same class pattern.','Substituting int and double produces different instantiations. Sharing the template definition does not make those types identical.'),('Yes; the template arguments disappear before C++ checks their member types.','The substituted type is used for the actual member and observer types; it is not erased before checking.'),('Yes; every Box object shares one stored T value.','Each box has its own member, and each instantiation has its chosen type. T is a placeholder in the definition, not one shared object.')]
}
for n,choices in QUESTION_REVISIONS.items():MODULES[n-1]['choices']=choices

class LiteralDumper(yaml.SafeDumper):pass
def represent_str(dumper,value):return dumper.represent_scalar('tag:yaml.org,2002:str',value,style='|' if '\n' in value else None)
LiteralDumper.add_representer(str,represent_str)

def migrate():
    destination=ROOT/'content/modules';destination.mkdir(exist_ok=True)
    for m in MODULES:
        # Remove obsolete v1 generation switches and generic help.
        for key in ['parsons','trace','hint']:m.pop(key,None)
        assert all(m['hints_by_type'].values()) and m.get('puzzle') and m.get('tracing')
        assert len(m['tracing']['expected'])==len(m['tracing']['values'])
        assert m['tracing']['output']==m['tracing']['expected'][0]
        (destination/(m['slug']+'.yaml')).write_text(yaml.dump(m,Dumper=LiteralDumper,sort_keys=False,allow_unicode=True,width=105),encoding='utf-8')
    (ROOT/'content/projects.yaml').write_text(yaml.dump(CAPSTONES,Dumper=LiteralDumper,sort_keys=False,allow_unicode=True,width=105),encoding='utf-8')
    print('Wrote 20 reviewed source modules and 2 reviewed projects.')

if __name__=='__main__':migrate()
