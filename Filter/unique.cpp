#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <unordered_map>
using namespace std;

unordered_map <string, bool> mp;
const string REPLACE = ", proxy";
int main() {
    std::ifstream inputFile("./rule");
    std::ofstream outputFile("./out_rule");

    if (!inputFile.is_open() || !outputFile.is_open()) {
        std::cerr << "无法打开文件。" << std::endl;
        return 1;
    }

    std::string line;
    while (std::getline(inputFile, line)) {
        if(mp[line]) continue;
        else {
            mp[line] = 1;
            outputFile << line << std::endl;
        }
    }

    inputFile.close();
    outputFile.close();

    return 0;
}