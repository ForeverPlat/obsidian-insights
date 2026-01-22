import os

vault_dir = "/Users/luqmanajani/documents/Notes/Obsidian-Vault"
# note_path = f"{vault_dir}/Intro to Databases.md"


def get_links(note):
    note_path = f"{vault_dir}/{note}.md"
    links = []

    try:
        with open(note_path, "r") as file:

            for line in file:

                while "[[" in line:
                    start = line.find("[[")
                    end = line.find("]]")

                    if end == -1:
                        break

                    link = line[start + 2 : end]
                    links.append(link)
                    line = line[end + 2 :]

                    # if word[0] == "[" and is_link == False:
                    #     is_link = True
                    #     word = word[2:]
                    #     print("word " + word)
                    #
                    # if is_link == True:
                    #
                    #     if word[-1] == "]":
                    #         word = word[:-2]
                    #         link += word
                    #         links.append(link)
                    #
                    #         is_link = False
                    #         link = ""
                    #         # print("\n")
                    #     else:
                    #         link += word + " "

    except:
        print(f"{note_path} does not exsist")

    return links


def search_connections(link):
    pass


# l = get_links("Obsidian Test")
# print(l)
# print(get_links(l[0]))

# print(get_links("Intro to Databases"))
print(get_links("Basics Of Technical Analysis FNCE"))
# print(get_links("Obsidian Test"))
