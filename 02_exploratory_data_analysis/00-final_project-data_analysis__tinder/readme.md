# Speed Dating Data Analysis
*Certification Bloc #2 — Data Science Training*

## 🎯 Project Objective

This project aims to explore a dataset from speed dating events to answer several key questions:

- Identify the least desirable attributes in a male and female partner.
- Study how important physical attractiveness is perceived versus its real impact.
- Compare the influence of shared interests versus shared racial background.
- Evaluate if participants can predict their perceived value in the dating market.
- Analyze whether being someone's first or last date of the evening influences the chances of getting a second date.

---

## 🛠️ Approach and Methodology

### 1. Exploratory Data Analysis and Cleaning

- Initial inspection of data dimensions and types.
- Handling missing values: analysis of NaN percentages and reasoned column removal.
- Normalization: adjustment of different scoring scales between waves.
- Data type corrections (casting to `category`, `int64`, etc.).
- Column renaming for better readability.

---

### 2. Data Exploration and Key Analyses

#### 🔹 Least desirable attributes by gender
- Analyzed average scores for attributes (`attr`, `sinc`, `intel`, `fun`, `amb`, `shar`) by gender.
- Highlighted which traits are less valued by males vs females.

#### 🔹 Perceived vs Real Importance of Attractiveness
- Compared the perceived importance (`attr1_1`, `attr2_1`, `attr4_1`) to real results (`match`, `like`, `dec`).

#### 🔹 Shared Interests vs Shared Race
- Investigated whether shared interests (`shar`) or shared racial background (`imprace`) had more influence on matches.

#### 🔹 Self-Perception vs Perceived Value
- Compared self-rated attributes (`attr5_1`, etc.) to how others actually rated participants.
- Measured and visualized the percentage differences.

#### 🔹 Impact of Speed Dating Order
- Analyzed whether being the first or last date of the night had an impact on second date likelihood.

---

## 📊 Visualizations Produced

- Comparative bar charts by gender.
- Pie charts showing attractiveness impact on matches and decisions.
- Heatmaps (importance of race vs religion).
- Subplots for self vs perceived ratings comparison.
- Scatter plots for missing data analysis.

---

## 📈 Key Results

- Least valued attributes differ slightly between men and women.
- Attractiveness is perceived as highly important (~32%) but has slightly less real impact (~55% vs 45%).
- Shared interests show a stronger real-world influence on matches than shared race.
- Participants tend to **overestimate** their attractiveness, sincerity, and intelligence by 8–13%.
- Being the first or last date does **not significantly impact** the likelihood of a second date.

---

## 📚 Deliverables

- Descriptive statistical analysis
- Relevant visualizations
- Captions and interpretations explaining how the data supports second date outcomes

---

## 🚀 Purpose of the Project

This project is part of my **Data Science training**.  
It aims to strengthen my skills in:

- Exploratory data analysis
- Data cleaning and transformation
- Advanced data visualization
- Interpretation of results in a real-world context

---

> 📌 *Project completed by Quentin Haentjens* — Le 26 avril 2025 dans le cadre de ma formation chez Jedha
