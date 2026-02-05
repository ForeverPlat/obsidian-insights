from commands.build import run_build
from commands.links import run_links
from commands.merge import run_merge
from commands.today import run_today

model_name = "all-MiniLM-L6-v2"
DB_PATH = "note.db"


# def print_connection(connection, max_lines=6):
#     divider = "━" * 60
#
#     print(divider)
#     print("\uf44c Suggested Connection")
#     print(divider)
#     print()
#     print(f"FROM : {connection['source_name']}")
#     print(f"TO   : {connection['target_name']}")
#     print(f"SCORE: {connection['score']:.2f}")
#     print()
#
#     def preview(text):
#         lines = [l.strip() for l in text.split("\n") if l.strip()]
#         return "\n".join(lines[:max_lines])
#
#     print(f"--- Evidence from {connection['source_name']} ---")
#     print(preview(connection["source_content"]))
#     print()
#
#     print(f"--- Evidence from {connection['target_name']} ---")
#     print(preview(connection["target_content"]))
#     print()

# def print_merge_candidate(candidate, max_lines=6):
#     divider = "━" * 60
#
#     print(divider)
#     print("󰐱 Possible Merge / Consolidation")
#     print(divider)
#     print()
#     print(f"NOTE A : {candidate['source_name']}")
#     print(f"NOTE B : {candidate['target_name']}")
#     print(f"SCORE  : {candidate['score']:.2f}")
#     print()
#
#     def preview(text):
#         lines = [l.strip() for l in text.split("\n") if l.strip()]
#         return "\n".join(lines[:max_lines])
#
#     print(f"--- Overlapping content in {candidate['source_name']} ---")
#     print(preview(candidate["source_content"]))
#     print()
#
#     print(f"--- Overlapping content in {candidate['target_name']} ---")
#     print(preview(candidate["target_content"]))
#     print()


# def obsidian_insights():
#     drop_all_tables()
#     init_all_schemas()
#
#     index_vault()
#     embed_segments()
#
#     segment_ids, similarity_matrix = compute_similarity(model_name)
#
#     if len(segment_ids) == 0:
#         print("No embeddings found, nothing to compute similarity on.")
#         return
#
#     similar_edges = extract_similar_edges(segment_ids, similarity_matrix)
#     missing_connections = find_relationships(similar_edges)["missing_connections"]
#     merge_candidates = find_relationships(similar_edges)["merge_candidates"]
#
#     for con in missing_connections:
#         print_connection(con)
#
#     print()
#     print("=====================")
#     print()
#
#     for can in merge_candidates:
#         print_merge_candidate(can)
#
#
# if __name__ == "__main__":
#     obsidian_insights()


def main(command, args):
    if command == "build":
        run_build(args)

    elif command == "today":
        run_today(args)

    elif command == "links":
        run_links(args)

    elif command == "merge":
        run_merge(args)

    else:
        print(f"Unknown command: {command}")
