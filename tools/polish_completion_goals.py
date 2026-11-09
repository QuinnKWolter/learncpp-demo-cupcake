"""One-time editorial addition; future edits belong in content/modules/*.yaml."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
GOALS=[
"Count all items in four boxes with three items in each, then print the total.",
"Make rectanglePerimeter return the distance around all four sides of the rectangle. The supplied main prints that returned number.",
"Exchange left and right while preserving both original values. Use the temporary value saved before either original changes.",
"Print a whole-number quotient followed by a fractional quotient for 15 divided by 4. Keep the fractional part in the second calculation.",
"Ask whether the text cupcake contains the smaller text cake anywhere inside it, and print the Boolean answer as a word.",
"Print true only when age is at least 12 and at most 17. Both endpoints belong to this range.",
"Let nextTicket remember its counter between calls, so successive calls return one and then two.",
"Add every integer from 1 through limit, including limit itself, then print the total once.",
"Read one integer and print valid only for scores from 0 through 100. Print invalid if reading fails or the number is outside the range.",
"Preserve a fractional quotient when dividing total by count. Converting the result after integer division would be too late.",
"Make the supplied larger template return the larger of its two arguments, using their chosen type.",
"Make addBonus change the caller's score by five through its parameter; main then reads the changed score through a valid pointer.",
"Print the parcel's weight only when its stored status is ready. Check the named status rather than inferring readiness from the weight.",
"Let Counter increase by one through its public increment method while keeping its stored member private.",
"Sort every element of the supplied vector into increasing order before printing it.",
"Make addBonus retain a copy of bonus when the lambda is created. Later changes to the original should not affect that saved copy.",
"Transfer the owned integer from first to second, so second owns it and first is empty afterward.",
"Make calls through Base references use the Derived implementation of value when the actual object is Derived.",
"Make the Box observer return the value stored in that object, keeping its chosen type and leaving the member unchanged.",
"Make checkedDivide reject a zero denominator with an exception while allowing division by a nonzero denominator, including a zero numerator."
]

if __name__=='__main__':
    paths=sorted((ROOT/'content/modules').glob('*.yaml'))
    assert len(paths)==len(GOALS)==20
    for path,goal in zip(paths,GOALS):
        text=path.read_text(encoding='utf-8')
        if 'completion_goal:' not in text:text+='\ncompletion_goal: '+json.dumps(goal,ensure_ascii=False)+'\n'
        text=text.replace('There is no missing pricing function, hidden calculation, or extra file for you to invent. Both files travel with the activity and are supplied to the compiler when you check an answer.','Read its body to see the whole calculation, then follow the returned number back to main. Both files are supplied when you check an answer.')
        path.write_text(text,encoding='utf-8')
