# Visual Design Principles

Core design principles for Power BI report visuals, synthesized from:
- *Storytelling with Data* (Knaflic, 2015)
- *Storytelling with Data: Let's Practice!* (Knaflic, 2020)
- *Data Visualization: A Handbook for Data Driven Design* (Kirk, 2nd ed., 2019)

---

## Three Universal Design Goals

Every visual must satisfy all three:

| Goal | Question to Ask | Key Responsibility |
|---|---|---|
| **Trustworthy** | Is the data handling faithful and accurate? | Honest encoding: zero-baseline bars, area for circles, equal-area maps |
| **Accessible** | Is it clear and friction-free for the audience? | Match complexity to audience; provide context and guides |
| **Elegant** | Is it considered, refined, and cohesive? | Remove the arbitrary; attend to alignment, spacing, and color |

---

## Pre-Attentive Attributes

Pre-attentive attributes are processed by the brain in under 250ms — *before* conscious attention.
Used strategically, they tell the audience **where to look** without requiring any reading.

### Attribute Inventory

| Attribute | Best For | Example Use in Power BI |
|---|---|---|
| **Color (hue)** | Categorical distinction; drawing attention | One accent hue for key data series; all others in grey |
| **Color intensity** | Quantitative magnitude | Heatmap cell shading; conditional formatting on tables |
| **Size** | Quantitative magnitude; relative importance | Larger font for headline KPI; bubble size in scatter chart |
| **Spatial position** | Quantitative comparison | Bar height/length; dot position on scatter |
| **Line length** | Quantitative comparison | Bar chart bars |
| **Line weight (width)** | Emphasis; hierarchy | Bold title vs. normal label; thick trend line vs. thin reference |
| **Shape** | Categorical distinction | Triangle vs. circle scatter markers for two groups |
| **Enclosure** | Grouping | Shaded background region grouping related visuals |
| **Added marks** | Highlighting anomalies | Data labels only on the highlighted bar |
| **Motion** | Drawing attention (use sparingly) | Animated KPI indication in executive dashboards |

### Rules for Pre-Attentive Attributes

1. **Use sparingly** — when everything stands out, nothing does. The power comes from contrast.
2. **One primary attribute per visual** — avoid competing attention signals (e.g., do not use
   both bold color AND size to emphasize two different things simultaneously).
3. **Color for emphasis, not decoration** — do not let Power BI's default multi-color palette
   apply; explicitly set colors to communicate meaning.
4. **Test the "3-second rule"** — show the visual for 3 seconds and ask: "What did you see
   first?" That must be the key insight.
5. **Quantitative attributes**: Size, position, length, and intensity can encode quantities.
   Hue (color type) cannot — it encodes categories only.

### "Where Are Your Eyes Drawn?" Test

Before finalizing any visual, cover the title and ask a colleague:
- Where do your eyes go first?
- What do you think this chart is about?
- What question does it raise?

If the answer is not the key insight, adjust pre-attentive attributes until attention lands there.

---

## Gestalt Principles for Report Layout

Gestalt principles describe how humans naturally group visual elements.
Apply them deliberately to guide reading flow and reduce cognitive load.

### Proximity
> Objects physically close together are perceived as belonging to the same group.

- Place data labels directly beside their data (eliminates the need for a legend)
- Cluster related KPI cards together; separate unrelated ones with white space
- Keep axis title close to the axis it describes
- Group related visuals on a page; use white space to separate conceptual sections

### Similarity
> Objects of similar color, shape, size, or orientation are perceived as related.

- Use the same color for all actual-value data series across all pages
- Use consistent visual types for equivalent data on different pages (same metric = same chart)
- Matching color between a legend label and its data element reinforces association

### Enclosure
> Objects physically enclosed together are perceived as belonging to a group.

- Use a background shape (`shape` visual) to visually group related visuals in a section
- Light grey shading behind filter controls separates them from the data area
- A subtle border or background color around a KPI row signals it as a distinct zone
- Does **not** require a border — even a slight shade change triggers the enclosure effect

### Closure
> The brain completes incomplete shapes, perceiving them as whole.

- Chart borders and background shading in Power BI are unnecessary — remove them;
  the audience perceives the visual as a cohesive unit without enclosing borders
- Removal bonus: the data stands out more against the white page

### Continuity
> The eye seeks a smooth path through visual elements.

- The vertical y-axis line can be removed; consistent bar alignment creates implied continuity
- Use dashed lines for forecasts vs. solid lines for actuals — both feel like "one line"
- Horizontal gridlines create continuity guides for reading bar heights across a chart

### Connection
> Physically connected objects are perceived as part of the same group
> (stronger associative value than similarity of color or shape).

- Lines in line charts connect dots into a perceived trend — stronger than scatter points alone
- Use a leader line (line from annotation text to a specific data point) for targeted callouts
- Color match a connection line + its endpoint to reinforce the association

---

## Color Theory for Data Visualization

### Color Models

**HSL (Hue-Saturation-Lightness)** — the preferred model for design decisions:
- **Hue**: The color type (red, blue, green…) — use for **categorical** data
- **Saturation**: Intensity/purity — high saturation = emphasis; low (grey) = background
- **Lightness**: Brightness — use for **quantitative** ordering (dark = high, light = low)

### When to Use Each Color Scale

| Scale Type | Use When | Example |
|---|---|---|
| **Sequential (single hue)** | Ordered data with one direction | Light blue → Dark blue for revenue deciles |
| **Diverging (two hues)** | Data with meaningful midpoint (zero, average, target) | Orange → White → Blue for profit/loss |
| **Categorical (distinct hues)** | Nominal groups needing distinction | Different hue per product line |

**Avoid rainbow (red→orange→yellow→green→blue)** scales for quantitative data — the
perceptual steps are not equal; green and blue both read as "high" without logical progression.

### Core Color Rules

1. **One accent color against grey** (the single most powerful technique):
   - Design the entire chart in shades of grey
   - Apply ONE bold color only to the data point / series that carries the key message
   - Everything else remains grey — grey is not "unimportant"; it is the canvas

2. **Use color consistently across the entire report**:
   - If blue = Sales, then blue = Sales on every page and every chart
   - Never reuse a color for a different category on different pages (forces re-learning)
   - Changing an established color signals a change — use this intentionally

3. **Limit total distinct colors per visual**:
   - Ideal: 1-2 accent colors + grey
   - Acceptable: up to 5-6 for categorical data with a clear legend
   - Avoid: rainbow palettes where each series gets a different color by default (Power BI default)
   - Rule of thumb: "At most 10% of the visual design should be highlighted"

4. **Colorblind accessibility** (~8% of men are red-green colorblind):
   - ❌ Avoid red + green as opposing signals (use for traffic-light KPIs with caution)
   - ✅ Blue + orange is a reliable, accessible high-contrast pairing
   - ✅ Add secondary encoding (icons, bold, plus/minus signs) alongside color
   - Test your theme: use Color Oracle (colororacle.org) or Coblis (color-blindness.com/coblis)

5. **Color conveys emotion — choose intentionally**:
   - Blues/teals: calm, trustworthy, analytical
   - Reds/oranges: urgency, warning, performance gap
   - Greens: growth, health, positive
   - Neutrals/greys: objective, professional, background context

6. **Sequential and diverging scales in Power BI**:
   - Conditional formatting on tables: use 3-color scale (min/mid/max) for diverging,
     2-color scale for sequential
   - For heatmaps: always specify the color scale endpoints explicitly rather than
     relying on auto-detected min/max

### Recommended Hex Palette Patterns

**Neutral base palette** (works for any industry when no custom theme is specified):
```
Primary accent:   #0070C0  (Microsoft blue — clear, accessible)
Grey scale:       #F2F2F2 (light), #BFBFBF (mid), #737373 (dark)
Positive:         #38B64B  (green — succeeded, growth, above target)
Negative:         #EE1C25  (red — failed, decline, below target)
Warning:          #FFB900  (amber — at risk, pending, attention needed)
Neutral/skipped:  #949599  (gray — skipped, inactive, no data)
Title text:       #1F1F1F
Label text:       #404040
Gridlines:        #E0E0E0
```

**Semantic color rules** — use consistently across all reports:

| Meaning | Color | Hex | When to Use |
|---|---|---|---|
| Succeeded / Good / Growth | Green | `#38B64B` | Status = passed, KPI above target, positive variance |
| Failed / Bad / Decline | Red | `#EE1C25` | Status = failed, KPI below target, negative variance |
| Warning / At Risk | Amber | `#FFB900` | Near threshold, pending review, caution needed |
| Skipped / Inactive / N/A | Gray | `#949599` | No data, not applicable, disabled, skipped |
| Info / In Progress | Blue | `#0078D4` | Active, running, informational, in progress |
| On Track / Neutral | Dark Gray | `#605E5C` | Within tolerance, expected, no change |

> For industry-specific palettes (8 industries) and ready-to-use theme JSON files,
> see [`theme-colors.md`](theme-colors.md) and `themes/*.json`.

**Alert/Warning pattern** (colorblind-safe alternative to red/green):
```
Positive/above target:  #0070C0  (blue)
Negative/below target:  #FF6D00  (orange)
Neutral/on track:       #737373  (grey)
```

---

## Clutter Reduction Checklist

Run through this list when designing each visual. Remove anything that earns a check.

### Chart Structure
- [ ] **Chart border** — remove unless the visual blends into an identical background color
- [ ] **Plot area background** — set to white or transparent; remove colored backgrounds
- [ ] **Heavy gridlines** — replace with very light grey (#E8E8E8) or remove entirely
- [ ] **Vertical gridlines** — almost always unnecessary on bar/column charts; remove
- [ ] **Tick marks on axes** — rarely needed; remove or reduce to minimal
- [ ] **Axis lines (spines)** — remove the top and right spines; often remove all

### Labels & Text
- [ ] **Redundant axis title** — if the chart title clearly states the metric, remove axis title
- [ ] **Trailing zeros on y-axis** (e.g., `1,000,000` vs. `1M`) — simplify
- [ ] **Diagonal text on axis labels** — rotate chart or reduce categories instead
- [ ] **Legend when direct labeling is possible** — label each series at its endpoint
- [ ] **Value labels on every data point** — label only the key/highlighted value(s)
- [ ] **Decimal precision beyond meaningful significance** — `42.73%` vs. `43%`
- [ ] **"All time" or "Total" in titles** — replace with meaningful period/scope

### Color & Visual Encoding
- [ ] **Default multi-color palette** — override; apply intent-driven color
- [ ] **More than 2 accent colors** — reduce to single accent + grey
- [ ] **Shadow, glow, or bevel effects** — remove (purely decorative)
- [ ] **Data markers on every point of a dense line** — show only at key events
- [ ] **Dual y-axis** — split into two vertically aligned charts instead

### Power BI Specific
- [ ] **Visual border in formatting pane** — off by default; leave off
- [ ] **Visual shadow** — off by default; leave off
- [ ] **Background color on visual** — only use if deliberately grouping visuals
- [ ] **Title underline** — remove styling; rely on size and weight for hierarchy
- [ ] **Tooltips with excessive detail** — keep tooltip to max 3-4 values

---

## Typography Hierarchy

Use consistent font sizing and weight to signal importance. Power BI default font is Segoe UI.

| Element | Font Size | Weight | Color | Notes |
|---|---|---|---|---|
| Page title (headline) | 18-24px | Bold | `#1F1F1F` | States the key insight; never just a label |
| Section heading | 14-16px | Bold | `#1F1F1F` | Groups a cluster of visuals |
| Visual title | 11-13px | Bold | `#333333` | Takeaway statement, not a data description |
| Axis title | 10-11px | Regular | `#595959` | Only when axis is not self-evident |
| Axis labels | 9-10px | Regular | `#595959` | Key values only; avoid rotating if possible |
| Data labels | 9-11px | Regular / Bold | Matches series color | Only on highlighted series |
| Legend | 9-10px | Regular | `#595959` | Remove if direct-labeling is possible |
| KPI card value | 28-48px | Bold | Theme accent | Largest text on page |
| KPI card label | 10-12px | Regular | `#595959` | Subtitle beneath the KPI value |
| Footnote / source | 8-9px | Regular | `#808080` | Attribution, date, caveats |

### Text Alignment Rules
- **Titles**: left-aligned (top-left is where eyes land first; F-pattern and Z-pattern reading)
- **Axis labels**: left-aligned for categories; right-aligned for numbers
- **KPI values**: center-aligned within their card is acceptable
- **Avoid center-aligned body text** — creates jagged edges ("hung text") that look unpolished
- **Never rotate text more than 45°** — forces head-tilting; transpose chart instead

---

## Visual Titles as Headlines

> "Takeaway titles tell the viewer what to think. Descriptive titles make the viewer do work."
> — *Storytelling with Data*

### Three Title Patterns

| Pattern | Type | Use When | Example |
|---|---|---|---|
| **Statement title** | Takeaway / action | Explanatory report; you have a finding | *"Revenue grew 42% YoY driven by Enterprise"* |
| **Question title** | Exploratory | Interactive dashboard; viewer investigates | *"Which regions are driving growth this quarter?"* |
| **Descriptive title** | Label / reference | Operational dashboard; viewer knows the metric | *"Monthly Revenue by Region"* |

**Preferred pattern for Power BI reports**: Statement titles on analytical pages;
question titles on interactive dashboards; descriptive titles only when the audience
will look up a specific number (not interpret a story).

### Rules
1. Titles must be complete sentences or noun phrases that convey a meaningful message
2. Never use just the metric name as a title (`"Revenue"` → `"Revenue Grew 40% YoY"`)
3. Match title to visual — if you can't write a takeaway, re-examine whether the visual
   is the right one
4. Use the same font weight/size as defined in the typography hierarchy
5. Upper-left justify all titles — this aligns with the Z-pattern reading flow

---

## Narrative Structure for Dashboard Pages

Each page should follow an implicit narrative arc:

```
┌─────────────────────────────────────────────────────────┐
│ HEADLINE (Z-pattern entry point)                        │
│ "What happened?" — 1 sentence insight in page title    │
│ + KPI cards showing the most important numbers          │
│ + Date/category context slicer                          │
├─────────────────────────────────────────────────────────┤
│ EVIDENCE (Primary visual zone)                          │
│ The chart that *proves* the headline statement.         │
│ One hero visual. One accent color on the key series.    │
│ Everything else in grey.                                │
├─────────────────────────────────────────────────────────┤
│ CONTEXT (Secondary visual zone)                         │
│ 1-3 supporting visuals that explain the "why" or        │
│ provide the comparison that makes the headline stick.   │
├─────────────────────────────────────────────────────────┤
│ DETAIL (Analysis zone)                                  │
│ Table or matrix for viewers who need to verify          │
│ numbers or explore at row level.                        │
├─────────────────────────────────────────────────────────┤
│ ACTION (Bottom zone)                                    │
│ Filters, navigation buttons, reset controls.            │
│ What should the viewer do next?                         │
└─────────────────────────────────────────────────────────┘
```

### Pre-Design Questions (answer before placing a single visual)

1. **WHO** is the audience? (executive / analyst / operator)
2. **WHAT** should they know or do after seeing this page?
   - Complete: *"I want my audience to ___"* in one sentence
   - If you can't complete this sentence, the page is not ready
3. **WHAT** data supports that message?
   - Select only data that advances the narrative — omit the rest
4. **WHAT** is the Big Idea?
   - A single sentence that (a) states a point of view, (b) conveys what's at stake,
     and (c) is complete enough to stand alone

---

## Audience Design Guide

Adjust design complexity based on the audience's consumption context:

### Executive / Leadership (Boardroom)
- **Goal**: Communicate the finding instantly; support a decision
- **Attention span**: 5-30 seconds per page
- **Design rules**:
  - Statement title = the conclusion
  - 3-5 KPI cards at top
  - One main chart proving the headline
  - Minimal annotation — no need to explain "how to read this chart"
  - Avoid scatter plots, small multiples, data tables as primary visuals
  - Font sizes larger than average; less dense layout

### Analyst / Detailed User
- **Goal**: Enable exploration; answer follow-up questions
- **Attention span**: 5-15 minutes per session
- **Design rules**:
  - Question titles ("What's driving the decline?")
  - Interactive slicers and drill-through
  - Scatter plots, small multiples, detail matrices are appropriate
  - Include data tables for row-level verification
  - Tooltips with additional metrics on hover

### Operational / Daily User (Dashboard/Cockpit)
- **Goal**: Check status quickly; identify what needs action
- **Attention span**: Repeated 30-second glances
- **Design rules**:
  - KPI cards with vs-target indicators at top
  - Trend line with reference line (target)
  - Color-coded status (alert = red/orange; on-track = neutral)
  - Minimal decorative elements; fast loading
  - Consistent layout across days — no surprises

### Mixed Audience
- Stratify with progressive disclosure:
  - Headline + KPIs visible to all (top of page)
  - Expandable detail or drillthrough for those who need depth
  - Tooltips reveal additional metrics without cluttering the main visual

---

## The 5-Layer Design Process

A sequential framework for building visualizations, based on
*Data Visualization* by Andy Kirk (2nd edition, 2019). Work through
layers in order — each layer builds on the previous.

### Layer 1: Data Representation (What chart?)

Choose the visual encoding that best matches the analytical task:

| Task | Representation | Power BI Visual |
|------|----------------|-----------------|
| Compare categories | Horizontal bars, ordered by value | Bar chart (sorted desc) |
| Show trend over time | Line, slope, connected dots | Line chart |
| Show parts of whole | Stacked bars, treemap | Stacked bar, treemap |
| Show distribution | Histogram, box-and-whisker | Histogram, box plot (custom) |
| Show correlation | Scatter, bubble | Scatter chart |
| Show geographic | Choropleth, dot map | Filled map, Azure map |
| Show flow / process | Sankey, funnel | Sankey (custom visual), Funnel |
| Show ranking | Ordered bar, lollipop | Bar chart (sorted), dumbbell custom |
| Show magnitude | Sized elements (area, bubble) | Bubble on scatter, card values |

**Decision rule**: Choose the simplest representation that answers the
question. If a bar chart works, use a bar chart — don't reach for a
more complex visual type.

### Layer 2: Interactivity (How does the user explore?)

Decide which interactive features to add (only if consuming digitally):

```
Interactivity Decision Tree:
1. Does the user need to filter by context? → Add slicers
2. Does the user need detail behind a summary? → Add drillthrough
3. Should one visual filter others? → Enable cross-filtering (default)
4. Does the user need to compare scenarios? → Add bookmarks
5. Should the user choose which metrics to view? → Add field parameters
6. Is there a natural navigation sequence? → Add page tabs / buttons
```

**Kirk's principle:** Interactivity is not decoration. Each interactive feature
must unlock an analytical question the static view cannot answer. If the
static view is sufficient, do not add interactivity.

### Layer 3: Annotation (What text supports the data?)

Annotation provides the scaffolding that helps the viewer decode the visual.
Work through this hierarchy (most important first):

```
1. Title/headline     — What is this about? What's the takeaway?
2. Subtitle/context   — Time period, scope, comparison context
3. Direct labels      — Label the data point/series directly (avoid legends)
4. Axis titles        — Only if the axis is not self-evident
5. Reference lines    — Target, average, benchmark for comparison
6. Annotations/callouts — Specific events or anomalies worth noting
7. Footnote/source    — Data provenance, caveats, last refresh
```

**Kirk's hierarchy rule**: Every annotation has a cost (cognitive load) and
a benefit (clarity). Include an annotation only if the benefit exceeds the
cost. Work from the top of the hierarchy downward and stop when the
visual is self-explanatory.

### Layer 4: Color (How does color encode meaning?)

Apply color as the **second-to-last** layer. Decisions made here should
reinforce the choices already made in Layers 1-3:

```
Color Decision Sequence:
1. Start with everything in grey (no color)
2. Apply ONE accent color to the key data point/series (the insight)
3. If categories need distinction, assign semantic hue (max 5-6)
4. If magnitude needs encoding, use a sequential scale (light → dark)
5. For diverging data (above/below target), use a diverging scale
6. Test: does the visual work in greyscale? If not, you're over-relying on color
```

See the **Color Theory** section above for detailed rules and palettes.

### Layer 5: Composition (How is everything arranged on the page?)

The final layer addresses the overall layout:

```
Composition Checklist:
□ Z-pattern / F-pattern reading flow respected
□ Headline insight at top-left (first thing the eye hits)
□ KPI cards in the first row (most important numbers)
□ Hero visual immediately below the headline
□ Supporting visuals below or to the right
□ Slicers and filters in a consistent location (left panel or top strip)
□ White space used to separate conceptual groups (Gestalt proximity)
□ Consistent margins and alignment (no visual is "floating" off-grid)
□ Visual density is appropriate for the audience:
  - Executive: sparse (3-5 visuals per page)
  - Analyst: moderate (6-8 visuals per page)
  - Operational: focused (live KPIs + 2-3 action visuals)
```

**Kirk's composition principle:** Composition is the "frame" — it should be
invisible. The viewer should never notice the layout; they should only notice
the data. If the layout draws attention to itself (misaligned, crowded, overly
decorative), it's failing.

---

## Accessibility Design

Based on *Power BI — Create Reports* (Microsoft, 2025), Chapter: Design Power BI
reports for accessibility.

> **Principle:** Whenever building a report, no matter who your audience is,
> create reports usable by as many people as possible without special adaptation.

### Built-in Features (No Configuration Needed)

- **Keyboard navigation** — All Power BI visuals support keyboard navigation;
  focus indicator shows current position
- **Screen reader compatibility** — Every keyboard-navigable object works with
  screen readers (reads title, visual type, and alt text)
- **High contrast** — Power BI Desktop detects Windows high contrast settings
  and applies them automatically; these carry to the published report
- **Focus mode** — Consumers expand any visual to full screen
- **Show Data table** — `Alt+Shift+F11` displays visual data in a
  screen-reader-friendly table

### Author-Configurable Features

#### Alt Text
- Add alt text to **every non-decorative visual** (limit: 250 characters)
- Describe the **insight**, not the visual type (screen reader already announces
  the type and title)
- Example: *"Net user satisfaction by color of product sold, further broken down
  by product class"*
- Use **conditional formatting for dynamic alt text** — DAX measures can make
  alt text reflect current data
- When exporting to PowerPoint, alt text carries over (default: "No alt text provided")

#### Tab Order
- Set tab order in the **Selection pane → Tab order** tab
- Match the order in which users visually process the page (top-left to bottom-right)
- **Hide decorative shapes/images** from tab order so screen readers skip them

#### Titles and Labels
- Avoid acronyms or jargon in titles
- Use clear, complete titles that external users can understand

#### Markers (Lines and Scatter)
- For Line, Area, Combo, Scatter, and Bubble visuals: **turn on markers**
- Use a **different marker shape per series** (not just color)
- Prevents reliance on color alone for series distinction

#### Report Themes
- WCAG 2.1 criterion 1.4.3: text/background contrast ratio ≥ **4.5:1**
- Test with Color Contrast Analyzer, WebAIM, or Accessible Colors
- Avoid these hard-to-distinguish color pairs:
  green+red, green+brown, blue+purple, green+blue,
  light green+yellow, blue+grey, green+grey, green+black
- Use fewer colors or a monochrome palette to improve accessibility

### Accessibility Checklist (Run Before Publishing)

- [ ] Alt text on all non-decorative visuals
- [ ] Tab order set; decorative items hidden from tab order
- [ ] Color is NOT the only way information is conveyed (use text, icons, markers)
- [ ] Color contrast ≥ 4.5:1 between text and background
- [ ] No jargon or unexplained acronyms in titles
- [ ] Page tested with color vision deficiency simulator (Coblis, Color Oracle)
- [ ] Key information is NOT only accessible through an interaction
  (if so, pre-filter or rearrange visuals)
- [ ] Bookmarks navigable by keyboard
- [ ] Sort order on each visual is intentional (Show Data table inherits it)
- [ ] Tooltips used only for ancillary info (users with motor issues can't hover)
- [ ] No auto-playing video or audio
- [ ] Video has captions; audio has a transcript
- [ ] Slicer design is consistent across pages (same fonts, colors, position)
- [ ] Decorative shapes/images don't distract or clutter
