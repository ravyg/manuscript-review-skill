# Pass 4 — Literature & positioning

Assess whether the paper is correctly placed in its field. Missing key related work is a top
reason for desk rejection. Use web search/fetch if available; otherwise reason from the paper's
own reference list and flag that coverage could not be independently checked.

## Procedure
1. **Extract the topic + 5–10 search-term combinations** from the research question.
2. **Survey** (if web available): query scholarly sources (`site:arxiv.org`,
   `site:semanticscholar.org`, Google Scholar), find the key **survey papers** (goldmines for
   related work), the most-cited work in the subfield, and very recent (last 6–12 months) work a
   reviewer would expect to see.
3. **Gap analysis:** state the state-of-the-art in 2–3 paragraphs; what's missing that this paper
   addresses; how it differs from the closest work; and the objection a reviewer will raise
   ("how is this different from X?").
4. **Competitive landscape:** for each close paper — citation, 2-sentence summary, key
   difference, whether the paper should benchmark against it.
5. **Must-cite list:** foundational classics; direct competitors (omitting these signals
   ignorance); methodological foundations; recent work.

## Output into the findings object
- Missing citations / positioning problems → `priority_fixes[]` and `section_findings[]`
  (Related Work).
- Note in a scorecard entry for the **Novelty/Positioning** dimension.
- If a "first to" / "novel" claim is contradicted by existing work, hand it to Pass 3 as well.

## Guidelines
Be honest — if prior work already does this, say so now (better than a reviewer saying it). Be
specific about the gap. Recency matters: reviewers judge whether the latest work is covered.
