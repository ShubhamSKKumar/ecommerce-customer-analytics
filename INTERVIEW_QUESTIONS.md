# Data Analyst Interview Preparation

This document contains 40 interview questions (with answers) categorized by skill, plus 10 project-specific questions an interviewer might ask after seeing this portfolio project on your resume.

## Python (Pandas)

**1. What is the difference between a Pandas Series and a DataFrame?**
A Series is a one-dimensional array-like object holding any data type, whereas a DataFrame is a two-dimensional, size-mutable, and potentially heterogeneous tabular data structure with labeled axes (rows and columns). Think of a Series as a single column and a DataFrame as an entire table.

**2. How do you handle missing values in a dataset using Pandas?**
You can identify missing values using `.isnull().sum()`. To handle them, you can drop the rows/columns using `.dropna()` if the missing data is sparse, or you can impute (fill) the values using `.fillna()` with the mean, median, mode, or a placeholder value, depending on the context.

**3. What does the `groupby()` function do in Pandas?**
`groupby()` is used to split the data into groups based on some criteria. It allows you to apply an aggregation function (like `sum()`, `mean()`, or `count()`) to each group independently. For example, `df.groupby('category')['revenue'].sum()` calculates total revenue per category.

**4. How do you merge two DataFrames in Pandas?**
You use the `pd.merge()` function, which is similar to a SQL JOIN. You specify the DataFrames, the columns to join on (`on='customer_id'`), and the type of join (`how='left'`, `'inner'`, `'right'`, `'outer'`).

**5. What is the purpose of `apply()` in Pandas?**
`apply()` allows you to apply a custom function along an axis of the DataFrame (either row-wise or column-wise). It is useful for creating new columns based on complex logic that cannot be easily achieved with vectorized operations.

**6. Explain how to use `loc` and `iloc` for slicing data.**
`loc` is label-based, meaning you access rows and columns by their index labels or column names (e.g., `df.loc[0, 'revenue']`). `iloc` is integer-position based, meaning you access them by their numerical position (e.g., `df.iloc[0, 3]`).

**7. How would you find and remove duplicate rows in a DataFrame?**
To find duplicates, use `df.duplicated()`. To remove them, use `df.drop_duplicates(inplace=True)`.

**8. What is the difference between `merge()` and `concat()`?**
`merge()` combines DataFrames based on common columns or indices (like SQL JOIN), aligning data horizontally. `concat()` physically appends DataFrames together, either stacking them vertically (adding rows) or side-by-side (adding columns), without matching values.

## SQL

**9. What is the difference between `WHERE` and `HAVING`?**
`WHERE` filters rows before any grouping or aggregation takes place. `HAVING` filters groups after the `GROUP BY` clause and aggregation have been applied. You cannot use aggregate functions (like `SUM()`) in a `WHERE` clause, but you can in `HAVING`.

**10. Explain the different types of JOINs in SQL.**
*   **INNER JOIN:** Returns only rows that have matching values in both tables.
*   **LEFT JOIN:** Returns all rows from the left table, and the matched rows from the right table (NULL if no match).
*   **RIGHT JOIN:** Returns all rows from the right table, and matched rows from the left (NULL if no match).
*   **FULL OUTER JOIN:** Returns all rows when there is a match in either the left or right table.

**11. What is a Common Table Expression (CTE)?**
A CTE is a temporary result set defined within the execution scope of a single `SELECT`, `INSERT`, `UPDATE`, or `DELETE` statement. It is created using the `WITH` keyword. CTEs make complex queries much easier to read and maintain compared to nested subqueries.

**12. Explain Window Functions in SQL.**
Window functions perform calculations across a set of table rows that are somehow related to the current row, but unlike aggregate functions, they do not cause rows to become grouped into a single output row. Examples include `RANK()`, `ROW_NUMBER()`, and `LAG()`.

**13. What is the difference between `RANK()`, `DENSE_RANK()`, and `ROW_NUMBER()`?**
*   `ROW_NUMBER()`: Assigns a unique sequential integer to rows (1, 2, 3, 4).
*   `RANK()`: Assigns the same rank to identical values, but skips the next rank (1, 2, 2, 4).
*   `DENSE_RANK()`: Assigns the same rank to identical values, but does not skip the next rank (1, 2, 2, 3).

**14. What does the `LAG()` function do?**
`LAG()` provides access to a row at a given physical offset that comes before the current row. It is incredibly useful for calculating month-over-month growth by comparing current month revenue to the previous month's revenue without needing self-joins.

**15. What is a Primary Key and a Foreign Key?**
A Primary Key uniquely identifies each record in a table. A Foreign Key is a field in one table that links to the Primary Key of another table, establishing a relationship between the two tables and enforcing referential integrity.

**16. How do you optimize a slow SQL query?**
*   Ensure appropriate indexes exist on columns used in `WHERE`, `JOIN`, and `ORDER BY` clauses.
*   Avoid `SELECT *`; only select necessary columns.
*   Avoid using functions on indexed columns in the `WHERE` clause (which prevents index usage).
*   Use `EXPLAIN` or `EXPLAIN QUERY PLAN` to analyze the execution path.

## Statistics

**17. What is the difference between Mean and Median? When would you use one over the other?**
The mean is the average of all values, while the median is the middle value when sorted. You should use the median when the data contains extreme outliers (e.g., income or housing prices), as the mean is heavily skewed by outliers, whereas the median is robust.

**18. What is a p-value in hypothesis testing?**
The p-value is the probability of observing the given results (or more extreme) under the assumption that the null hypothesis is true. A low p-value (typically < 0.05) indicates strong evidence against the null hypothesis, leading you to reject it.

**19. What is the difference between Correlation and Causation?**
Correlation means two variables move together (e.g., ice cream sales and shark attacks both increase in summer). Causation means one event is the direct result of the other. Correlation does not imply causation; there may be a confounding variable (like temperature).

**20. What is an outlier, and how do you handle it?**
An outlier is a data point that differs significantly from other observations. You can detect them using Z-scores or the IQR (Interquartile Range) method. You handle them by investigating if they are errors (and dropping/correcting them) or legitimate anomalies (in which case you might cap them or use robust statistics like the median).

**21. Explain the Null Hypothesis (H0) and Alternative Hypothesis (H1).**
The Null Hypothesis (H0) states that there is no significant difference, effect, or relationship (e.g., "Discount does not affect order value"). The Alternative Hypothesis (H1) states that there is a significant difference or effect (e.g., "Discount affects order value"). The goal of a statistical test is to determine if there is enough evidence to reject H0.

**22. What is standard deviation?**
Standard deviation is a measure of the amount of variation or dispersion in a set of values. A low standard deviation indicates that values tend to be close to the mean, while a high standard deviation indicates that values are spread out over a wider range.

## Power BI

**23. What is DAX in Power BI?**
DAX (Data Analysis Expressions) is a collection of functions, operators, and constants used to build formulas and expressions in Power BI. It is used to create custom calculations, measures, and calculated columns.

**24. What is the difference between a Calculated Column and a Measure?**
A Calculated Column is evaluated row-by-row during data refresh, consuming memory and increasing file size. A Measure is evaluated on-the-fly based on the context of the visual (e.g., slicers and rows), consuming CPU power during rendering but saving memory. You use Measures for aggregations (like Total Sales).

**25. What is a Star Schema? Why is it important?**
A Star Schema is a data modeling approach where a central "Fact" table (containing transactional data like orders) is surrounded by "Dimension" tables (containing descriptive attributes like customers or products). It is important because it simplifies queries, improves reporting performance, and is highly optimized for Power BI's VertiPaq engine.

**26. Explain the `CALCULATE()` function in DAX.**
`CALCULATE()` is the most powerful function in DAX. It evaluates an expression in a modified filter context. For example, `CALCULATE(SUM(Sales), Country="USA")` overrides any other filters on the Country column to only sum sales for the USA.

**27. What is the difference between `SUM()` and `SUMX()`?**
`SUM()` aggregates a single column. `SUMX()` is an iterator function; it evaluates an expression row-by-row over a specified table and then sums the results. For example, `SUMX(OrderItems, OrderItems[Qty] * OrderItems[Price])`.

**28. What are Slicers in Power BI?**
Slicers are interactive visual filters placed directly on the report canvas. They allow users to filter the data displayed in other visuals on the page (e.g., by selecting a specific year or product category).

## Business Analytics

**29. What is RFM Analysis?**
RFM stands for Recency, Frequency, and Monetary value. It is a marketing technique used to quantitatively segment customers based on their purchasing behavior. Recency is how recently they bought, Frequency is how often they buy, and Monetary is how much they spend.

**30. How do you calculate Customer Lifetime Value (CLV)?**
While complex predictive models exist, a simple heuristic calculation is: `Average Order Value × Purchase Frequency × Expected Customer Lifespan`. CLV helps businesses determine how much they can afford to spend on customer acquisition (CAC).

**31. What is Churn Rate?**
Churn rate is the percentage of customers who stop doing business with an entity over a given period. It is critical to track because acquiring new customers is significantly more expensive than retaining existing ones.

**32. How do you define a Key Performance Indicator (KPI)?**
A KPI is a quantifiable measure used to evaluate the success of an organization or project in meeting its strategic objectives. A good KPI should be specific, measurable, actionable, and aligned with business goals (e.g., "Increase Repeat Customer Rate by 5%").

---

## 10 Project-Specific Questions

**If this project is on your resume, be prepared to answer these:**

**33. Walk me through your E-Commerce Customer Analytics project from start to finish.**
*Answer strategy: Start with the business problem (understanding retention). Explain the data source (UCI dataset), the cleaning steps (handling missing IDs, returns), creating the SQLite database. Mention writing SQL for core metrics, using Python for RFM segmentation, and finally visualizing actionable insights in Power BI.*

**34. Why did you choose RFM for customer segmentation instead of a machine learning clustering algorithm like K-Means?**
*Answer strategy: Emphasize business interpretability. RFM provides clear, actionable rules that a marketing team immediately understands (e.g., "Champions" vs "At-Risk"). K-Means can create abstract clusters that are difficult to explain to non-technical stakeholders. In business analytics, interpretability often trumps complexity.*

**35. I see you handled negative quantities during data cleaning. Why did those exist in the data?**
*Answer strategy: In e-commerce datasets (specifically the UCI one), negative quantities usually represent returns or canceled orders (indicated by 'C' in the InvoiceNo). Removing them, or handling them separately as a "return rate" metric, is crucial so they don't artificially deflate revenue calculations.*

**36. How did you define an "At-Risk" customer in your RFM model?**
*Answer strategy: Explain the specific thresholds you used. For example, "I assigned an At-Risk label to customers whose Recency score was low (e.g., haven't purchased in over 90 days) but historically had high Frequency and Monetary scores. These are previously valuable customers who are showing signs of churning."*

**37. What was the most interesting insight you found during the Exploratory Data Analysis (EDA)?**
*Answer strategy: Pick a specific insight from your `business_insights.md`. For example: "I was surprised to find that while 20% discounts slightly increased Average Order Value, they significantly decreased overall profit margin compared to 5% discounts, indicating the promotion strategy needed a revamp."*

**38. Why did you create a Star Schema in Power BI instead of just importing the flat CSV?**
*Answer strategy: A flat table with 500,000 rows causes redundant data storage (like repeating the customer's name on every transaction). A Star Schema normalizes the data into Fact and Dimension tables, drastically improving Power BI's performance, memory usage, and making DAX filtering much easier.*

**39. Can you explain the SQL you wrote to find the Month-over-Month (MoM) revenue growth?**
*Answer strategy: Explain the `LAG()` window function. "I first aggregated the total revenue by month in a CTE. Then, in the main query, I used the `LAG(revenue) OVER (ORDER BY month)` function to pull the previous month's revenue into the same row as the current month's revenue, allowing me to calculate the percentage difference easily."*

**40. If the business stakeholders asked you how to improve the Retention Rate based on your findings, what would you suggest?**
*Answer strategy: Point to your recommendations. "Based on the RFM analysis, I would recommend setting up automated email triggers for the 'Potential Loyalists' to drive their frequency up, and exclusive win-back discounts tailored specifically to the 'At-Risk' segment before they become completely 'Lost'."*

**41. Did you face any challenges dealing with this dataset?**
*Answer strategy: Mention data quality issues. "Yes, there were thousands of records with missing Customer IDs. I had to decide whether to impute them or drop them. Since the goal was customer-centric analytics (RFM), a transaction without a Customer ID is useless, so I chose to drop them to maintain data integrity."*

**42. How would you automate this pipeline if it were put into production?**
*Answer strategy: Show forward-thinking. "Instead of manual Python scripts, I would use a workflow orchestration tool like Apache Airflow to schedule the ingestion and cleaning scripts to run nightly. I would migrate the SQLite database to a cloud data warehouse like Snowflake or BigQuery, and set Power BI to automatically refresh via an on-premises data gateway or direct query."*
