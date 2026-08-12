import nbformat as nbf
import os


def create_notebooks():
    os.makedirs("notebooks", exist_ok=True)

    # ---------------------------------------------------------
    # 01_eda.ipynb
    # ---------------------------------------------------------
    nb_eda = nbf.v4.new_notebook()
    nb_eda.cells = [
        nbf.v4.new_markdown_cell(
            "# Exploratory Data Analysis (EDA)\nIn this notebook, we analyze the cleaned and engineered E-Commerce dataset."
        ),
        nbf.v4.new_code_cell(
            "import pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport os\n\n# Set plotting style\nsns.set_theme(style='whitegrid')"
        ),
        nbf.v4.new_code_cell(
            "df = pd.read_csv('../data/cleaned/online_retail_features.csv')\ndf['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])\ndf.head()"
        ),
        nbf.v4.new_markdown_cell("## 1. Sales Trends"),
        nbf.v4.new_code_cell(
            "monthly_revenue = df.groupby('InvoiceMonth')['Revenue'].sum().reset_index()\nplt.figure(figsize=(12, 6))\nsns.barplot(data=monthly_revenue, x='InvoiceMonth', y='Revenue', color='steelblue')\nplt.title('Monthly Revenue Trend')\nplt.xticks(rotation=45)\nplt.show()"
        ),
        nbf.v4.new_markdown_cell("## 2. Customer Behavior"),
        nbf.v4.new_code_cell(
            "customer_spend = df.groupby('CustomerID')['Revenue'].sum()\nplt.figure(figsize=(10, 5))\nsns.histplot(customer_spend[customer_spend < 10000], bins=50, kde=True)\nplt.title('Distribution of Customer Total Spend (under $10,000)')\nplt.xlabel('Total Spend')\nplt.show()"
        ),
        nbf.v4.new_markdown_cell("## 3. Product Performance"),
        nbf.v4.new_code_cell(
            "top_products = df.groupby('Description')['Revenue'].sum().sort_values(ascending=False).head(10)\nplt.figure(figsize=(10, 6))\nsns.barplot(x=top_products.values, y=top_products.index, palette='viridis')\nplt.title('Top 10 Products by Revenue')\nplt.xlabel('Total Revenue')\nplt.show()"
        ),
    ]
    with open("notebooks/01_eda.ipynb", "w") as f:
        nbf.write(nb_eda, f)

    # ---------------------------------------------------------
    # 02_rfm_analysis.ipynb
    # ---------------------------------------------------------
    nb_rfm = nbf.v4.new_notebook()
    nb_rfm.cells = [
        nbf.v4.new_markdown_cell(
            "# RFM Customer Segmentation\nAnalyzing Recency, Frequency, and Monetary value of customers."
        ),
        nbf.v4.new_code_cell(
            "import pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns"
        ),
        nbf.v4.new_code_cell(
            "rfm = pd.read_csv('../data/cleaned/customer_segments.csv')\nrfm.head()"
        ),
        nbf.v4.new_markdown_cell("## Segment Distribution"),
        nbf.v4.new_code_cell(
            "segment_counts = rfm['Segment'].value_counts()\nplt.figure(figsize=(10, 6))\nsns.barplot(y=segment_counts.index, x=segment_counts.values, palette='coolwarm')\nplt.title('Customer Distribution by RFM Segment')\nplt.xlabel('Number of Customers')\nplt.show()"
        ),
        nbf.v4.new_markdown_cell("## RFM Value by Segment"),
        nbf.v4.new_code_cell(
            "rfm_agg = rfm.groupby('Segment').agg({\n    'Recency': 'mean',\n    'Frequency': 'mean',\n    'Monetary': 'mean',\n    'CustomerID': 'count'\n}).round(1)\nrfm_agg.rename(columns={'CustomerID': 'Count'}, inplace=True)\nrfm_agg.sort_values('Monetary', ascending=False)"
        ),
    ]
    with open("notebooks/02_rfm_analysis.ipynb", "w") as f:
        nbf.write(nb_rfm, f)

    # ---------------------------------------------------------
    # 03_statistical_analysis.ipynb
    # ---------------------------------------------------------
    nb_stat = nbf.v4.new_notebook()
    nb_stat.cells = [
        nbf.v4.new_markdown_cell(
            "# Statistical Analysis\nTesting business hypotheses using statistical methods."
        ),
        nbf.v4.new_code_cell(
            "import pandas as pd\nimport sqlite3\nfrom scipy import stats"
        ),
        nbf.v4.new_code_cell(
            'conn = sqlite3.connect(\'../ecommerce.db\')\nquery = """\nSELECT \n    c.customer_id,\n    COUNT(DISTINCT o.order_id) as order_count,\n    SUM(oi.revenue) as total_revenue\nFROM customers c\nJOIN orders o ON c.customer_id = o.customer_id\nJOIN order_items oi ON o.order_id = oi.order_id\nGROUP BY c.customer_id\n"""\ncustomer_data = pd.read_sql(query, conn)\nconn.close()\ncustomer_data.head()'
        ),
        nbf.v4.new_markdown_cell(
            "## Hypothesis: Do repeat customers spend significantly more overall than one-time customers?\n- **H0:** There is no significant difference in total revenue between one-time and repeat customers.\n- **H1:** Repeat customers spend significantly more."
        ),
        nbf.v4.new_code_cell(
            "one_time = customer_data[customer_data['order_count'] == 1]['total_revenue']\nrepeat = customer_data[customer_data['order_count'] > 1]['total_revenue']\n\nt_stat, p_val = stats.ttest_ind(repeat, one_time, equal_var=False)\nprint(f'T-statistic: {t_stat:.4f}')\nprint(f'P-value: {p_val:.4e}')\n\nif p_val < 0.05:\n    print('Reject H0: There is a significant difference in revenue.')\nelse:\n    print('Fail to reject H0: No significant difference.')"
        ),
    ]
    with open("notebooks/03_statistical_analysis.ipynb", "w") as f:
        nbf.write(nb_stat, f)

    print("Notebooks generated successfully.")


if __name__ == "__main__":
    create_notebooks()
