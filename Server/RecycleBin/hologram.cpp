#include <iostream>
#include <fstream>
#include <unistd.h> // for sleep
#include <jsoncpp/json/json.h> // JSON library, you may need to install it

enum class Color { DEFAULT, RED, YELLOW, BLUE };

class NeuralHologram {
private:
    std::string last_face;
    Color last_colour;

    std::string loadFaceFromFile(const std::string& filename) {
        std::ifstream file(filename);
        std::string expression;
        if (file.is_open()) {
            file >> expression;
            file.close();
        }
        return expression;
    }

    Color loadColorFromSettings(const std::string& filename) {
        Json::Value root;
        Json::Reader reader;
        std::ifstream config(filename);
        if (!reader.parse(config, root, false))
            return Color::DEFAULT;

        std::string colorStr = root["colour"].asString();
        if (colorStr == "RED") return Color::RED;
        if (colorStr == "YELLOW") return Color::YELLOW;
        if (colorStr == "BLUE") return Color::BLUE;
        return Color::DEFAULT;
    }

    void displayFace(const std::string& face, Color color) {
        switch (color) {
            case Color::RED:
                std::cout << "\033[31m" << face << "\033[0m"; // Red color
                break;
            case Color::YELLOW:
                std::cout << "\033[33m" << face << "\033[0m"; // Yellow color
                break;
            case Color::BLUE:
                std::cout << "\033[34m" << face << "\033[0m"; // Blue color
                break;
            default:
                std::cout << face;
        }
    }

public:
    NeuralHologram() : last_colour(Color::DEFAULT) {}

    void activate() {
        while (true) {
            std::string recent_expression = loadFaceFromFile("./Short_Term_Memory/face.txt");
            Color recent_colour = loadColorFromSettings("./Settings/configuration.json");

            if (last_face != recent_expression || last_colour != recent_colour) {
                last_face = recent_expression;
                last_colour = recent_colour;
                system("clear");
                displayFace(last_face, last_colour);
            }
            sleep(1); // Sleep for 1 second
        }
    }
};

int main() {
    NeuralHologram hologram;
    hologram.activate();
    return 0;
}
