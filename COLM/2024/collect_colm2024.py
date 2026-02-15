"""Collect COLM 2024 reviews and full discussion threads from OpenReview; save CSV to COLM/2024."""
import openreview
import pandas as pd
import tqdm
from collections import defaultdict
from pathlib import Path


def get_all_descendants(root_id, reply_map):
    descendants = []
    for child in reply_map.get(root_id, []):
        descendants.append(child)
        descendants.extend(get_all_descendants(child.id, reply_map))
    return descendants


def get_full_conversation(client, venue_id, submission_invitation):
    print(f"1. Getting submission list ({submission_invitation})...")
    submissions = client.get_all_notes(invitation=submission_invitation)
    print(f"2. Found {len(submissions)} submissions.")

    all_reviews_data = []

    for note in tqdm.tqdm(submissions):
        paper_id = note.id
        paper_title = note.content.get("title", {}).get("value")
        paper_number = note.number

        forum_notes = client.get_all_notes(forum=paper_id)
        reply_map = defaultdict(list)
        reviews = []
        decision_note = None

        for n in forum_notes:
            if n.replyto:
                reply_map[n.replyto].append(n)
            if n.invitations and any("Decision" in inv for inv in n.invitations):
                decision_note = n
            # Match Official_Review (ICLR) or .../Review (COLM and others)
            if n.invitations and (
                any("Official_Review" in inv for inv in n.invitations)
                or any(
                    inv.endswith("/Review") or inv.endswith("/Official_Review")
                    for inv in (n.invitations or [])
                )
            ):
                reviews.append(n)

        decision_value = "None"
        if decision_note:
            decision_value = decision_note.content.get("decision", {}).get("value", "None")

        for review in reviews:
            review_id = review.id
            review_content = review.content
            discussion_nodes = get_all_descendants(review_id, reply_map)
            discussion_nodes.sort(key=lambda x: x.tmdate)

            transcript_lines = []
            if discussion_nodes:
                for node in discussion_nodes:
                    speaker = "Unknown"
                    sigs = node.signatures or []
                    if any("Authors" in s for s in sigs):
                        speaker = "Authors"
                    elif any("Reviewer" in s for s in sigs):
                        speaker = sigs[0].split("/")[-1]
                    elif any("Area_Chair" in s for s in sigs):
                        speaker = "Area Chair"
                    text = node.content.get("comment", {}).get("value", "") or node.content.get("review", {}).get("value", "")
                    transcript_lines.append(f"[{speaker}]: {text}")
                discussion_transcript = "\n\n".join(transcript_lines)
            else:
                discussion_transcript = "None"

            all_reviews_data.append({
                "paper_number": paper_number,
                "paper_title": paper_title,
                "decision": decision_value,
                "review_id": review_id,
                "rating": review_content.get("rating", {}).get("value"),
                "confidence": review_content.get("confidence", {}).get("value"),
                "review_text": review_content.get("review", {}).get("value"),
                "discussion_transcript": discussion_transcript,
            })

    return pd.DataFrame(all_reviews_data)


def main():
    client = openreview.api.OpenReviewClient(baseurl="https://api2.openreview.net")
    venue_id = "colmweb.org/COLM/2024/Conference"
    submission_invitation = f"{venue_id}/-/Submission"

    df = get_full_conversation(client, venue_id, submission_invitation)

    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / "colm2024_full_transcript.csv"

    print("\n---------------- COLM 2024 RESULTS ----------------")
    if not df.empty:
        print(f"Collected {len(df)} reviews with full conversation threads.")
        df.to_csv(out_path, index=False)
        print(f"Saved to {out_path}")
    else:
        print("No data found.")


if __name__ == "__main__":
    main()
