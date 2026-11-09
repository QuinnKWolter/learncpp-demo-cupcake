"""Run actual language/library probes with the exact compiler used by the browser service."""
from pathlib import Path
import json
from execution import run_source,COMPILER,STANDARD,invoke,ROOT,REPORTS

source=r'''
#include <iostream>
#include <string>
#include <expected>
#include <utility>
#include <version>
static_assert(__cplusplus >= 202302L, "A C++23-capable compiler is required");
constexpr int choose() { if consteval { return 23; } else { return 0; } }
enum class Status { ready = 3 };
int main() {
    static_assert(choose()==23);
    std::string word{"cupcake"};
    std::expected<int, std::string> result{7};
    std::cout << __cplusplus << ' ' << word.contains("cake") << ' '
              << std::to_underlying(Status::ready) << ' ' << result.value() << '\n';
}
'''
result=run_source(source,[dict(title='C++23 language and library',stdin=[],stdout='202302 1 3 7\n')])[0]
if not result['passed']:raise SystemExit(result)
version=invoke([COMPILER,'--version'],ROOT)['stdout'].splitlines()[0]
report=dict(compiler=COMPILER,version=version,standard=STANDARD,cpp=202302,
            verified=['C++23 language mode','if consteval','string::contains','to_underlying','expected'],result=result)
REPORTS.mkdir(parents=True,exist_ok=True)
(REPORTS/'cpp23-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(version);print('C++23 probes passed:',result['stdout'].strip())
