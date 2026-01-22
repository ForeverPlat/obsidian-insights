import os

vault_dir = "/Users/luqmanajani/documents/Notes/Obsidian-Vault"
# note_path = f"{vault_dir}/Intro to Databases.md"


def get_links(note):
    note_path = f"{vault_dir}/{note}.md"
    links = []

    try:
        with open(note_path, "r") as file:

            for line in file:

                is_link = False
                link = ""

                for word in line.split():

                    if "[[" in word:
                        is_link = True

                    if is_link:
                        i = 0
                        while True:
                            if i >= len(word):
                                link += " "
                                break

                            if word[i : i + 2] == "]]":
                                # print(link)
                                links.append(link)
                                link = ""
                                is_link = False
                                break

                            if word[i] not in ["[", "]", "*", "_", '"']:
                                link += word[i]
                            i += 1

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
