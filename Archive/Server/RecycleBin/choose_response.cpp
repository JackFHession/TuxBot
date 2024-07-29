#include <iostream>
#include <fstream> // Include fstream library for file operations
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/algorithm/string.hpp>
#include <regex> // Include regex library for pattern matching
#include <random> // Include random library for random selection

using namespace std;
using namespace boost::property_tree;

// Function to calculate similarity between two strings
double similarity(const string& input, const string& pattern) {
    // Remove punctuation symbols from both strings
    string inputProcessed = regex_replace(input, regex("[[:punct:]]"), "");
    string patternProcessed = regex_replace(pattern, regex("[[:punct:]]"), "");

    // Convert both processed strings to lowercase for case-insensitive comparison
    string inputLower = inputProcessed;
    string patternLower = patternProcessed;
    boost::algorithm::to_lower(inputLower);
    boost::algorithm::to_lower(patternLower);

    // Calculate similarity using a simple approach (e.g., exact match)
    return (inputLower == patternLower) ? 1.0 : 0.0;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        cout << "Usage: " << argv[0] << " \"Your message\"" << endl;
        return 1;
    }

    try {
        // Load the JSON file into the property tree
        ptree pt;
        read_json("short_term_memory/current_class.json", pt);

        string userInput = argv[1]; // Get the input from command-line argument

        double maxSimilarity = 0.0;
        string bestMatchResponse;
        vector<string> matchingResponses;

        // Accessing 'responses' array and iterating over its elements
        for (const auto& response : pt.get_child("responses")) {
            double similarityScore = similarity(userInput, response.second.get_value<string>());
            if (similarityScore > maxSimilarity) {
                maxSimilarity = similarityScore;
                bestMatchResponse = response.second.get_value<string>();
            } else if (similarityScore == maxSimilarity) {
                matchingResponses.push_back(response.second.get_value<string>());
            }
        }

        if (maxSimilarity > 0.0) {
            cout << "Best Match Response: " << bestMatchResponse << " (Similarity: " << maxSimilarity << ")" << endl;

            // Write the response to a file
            ofstream outputFile("short_term_memory/output.txt");
            if (outputFile.is_open()) {
                outputFile << bestMatchResponse << endl;
                outputFile.close();
            } else {
                cerr << "Error: Unable to open file for writing." << endl;
            }
        } else {
            if (!matchingResponses.empty()) {
                // If there are multiple matching responses, choose one randomly
                random_device rd;
                mt19937 gen(rd());
                uniform_int_distribution<> dis(0, matchingResponses.size() - 1);
                int randomIndex = dis(gen);
                cout << "Random Response: " << matchingResponses[randomIndex] << endl;

                // Write the response to a file
                ofstream outputFile("short_term_memory/output.txt");
                if (outputFile.is_open()) {
                    outputFile << matchingResponses[randomIndex] << endl;
                    outputFile.close();
                } else {
                    cerr << "Error: Unable to open file for writing." << endl;
                }
            } else {
                cout << "No matching response found." << endl;

                // Write a message to indicate no matching response to the file
                ofstream outputFile("short_term_memory/output.txt");
                if (outputFile.is_open()) {
                    outputFile << "No matching response found." << endl;
                    outputFile.close();
                } else {
                    cerr << "Error: Unable to open file for writing." << endl;
                }
            }
        }

    } catch (const std::exception& ex) {
        cerr << "Error: " << ex.what() << endl;
        return 1;
    }

    return 0;
}
