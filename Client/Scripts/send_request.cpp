#include <iostream>
#include <string>
#include <curl/curl.h>
#include <nlohmann/json.hpp>
#include <fstream>
#include <filesystem>

using json = nlohmann::json;
namespace fs = std::filesystem;

size_t WriteCallback(void *contents, size_t size, size_t nmemb, std::string *output) {
    output->append((char*)contents, size * nmemb);
    return size * nmemb;
}

void SaveResponseToFile(const std::string& response) {
    std::ofstream file("./local_memory/current_class.json");
    if (file.is_open()) {
        file << response;
        file.close();
        std::cout << "Response saved to file." << std::endl;
    } else {
        std::cerr << "Failed to open file for writing." << std::endl;
    }
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <URL> <message>" << std::endl;
        return 1;
    }

    std::string url = argv[1];
    std::string message = argv[2];

    // Construct JSON object
    json message_data;
    message_data["message"] = message;
    std::string message_json = message_data.dump();

    // Set up libcurl
    CURL *curl;
    CURLcode res;
    curl_global_init(CURL_GLOBAL_ALL);
    curl = curl_easy_init();
    std::string output; // Declaration of output variable
    if (curl) {
        struct curl_slist *headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");

        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, message_json.c_str());
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &output);

        res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        }

        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);

        SaveResponseToFile(output); // Save response to file
    }

    curl_global_cleanup();

    return 0;
}

