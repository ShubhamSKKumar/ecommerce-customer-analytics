import streamlit as st
import pandas as pd
import sqlite3
import os
import plotly.express as px
import plotly.graph_objects as go
import sys

# Add src to path so we can import from config and scripts
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from src import config

st.set_page_config(
    page_title="E-Commerce Customer Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. INITIALIZATION LOGIC ---
@st.cache_resource
def initialize_pipeline():
    """Run the data pipeline if the database or segments file is missing."""
    db_exists = os.path.exists(config.DB_PATH)
    segments_exists = os.path.exists(config.SEGMENTS_CSV_PATH)
    
    if db_exists and segments_exists:
        return True
        
    placeholder = st.empty()
    with placeholder.container():
        st.info("First run detected. Initializing dataset and pipeline. This may take a few minutes...")
        progress_bar = st.progress(0)
        
        try:
            from src.data_ingestion import download_and_extract_data
            from src.data_cleaning import clean_data
            from src.feature_engineering import engineer_features
            from src.database_setup import create_database
            from src.rfm_segmentation import calculate_rfm
            
            st.text("1. Downloading and extracting data...")
            download_and_extract_data()
            progress_bar.progress(20)
            
            st.text("2. Cleaning data...")
            clean_data()
            progress_bar.progress(40)
            
            st.text("3. Engineering features...")
            engineer_features()
            progress_bar.progress(60)
            
            st.text("4. Creating SQLite database...")
            create_database()
            progress_bar.progress(80)
            
            st.text("5. Calculating RFM segments...")
            calculate_rfm()
            progress_bar.progress(100)
            
            st.success("Pipeline initialized successfully!")
            return True
            
        except Exception as e:
            st.error(f"Error during initialization: {str(e)}")
            initialize_pipeline.clear()
            st.stop()
        finally:
            # We don't want to show this forever
            placeholder.empty()

# --- 2. DATA LOADING ---
@st.cache_resource
def get_db_connection():
    return sqlite3.connect(config.DB_PATH, check_same_thread=False)

@st.cache_data
def load_data(query):
    conn = get_db_connection()
    return pd.read_sql(query, conn)

@st.cache_data
def load_rfm_data():
    return pd.read_csv(config.SEGMENTS_CSV_PATH)

# Run initialization
initialize_pipeline()

# --- 3. HELPER FUNCTIONS ---
def format_currency(value):
    return f"${value:,.2f}"

def format_number(value):
    return f"{value:,.0f}"

# --- 4. NAVIGATION & SIDEBAR ---
with st.sidebar:
    st.title("📈 E-Commerce Analytics")
    st.markdown("Retention Intelligence Dashboard")
    st.markdown("---")
    
    pages = [
        "Executive Overview",
        "Customer Intelligence",
        "Product & Business Analytics",
        "Retention & Customer Behavior",
        "SQL Analytics"
    ]
    selected_page = st.radio("Navigation", pages, label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### ℹ️ About this project")
    st.markdown(
        """
        An end-to-end analytics pipeline transforming **~541K raw transactions** 
        from the UCI Online Retail dataset into actionable intelligence.
        
        **Tech Stack:**
        - Python, Pandas, NumPy
        - SQLite, SQL
        - Streamlit, Plotly
        - RFM Segmentation
        """
    )

# --- 5. PAGE IMPLEMENTATIONS ---
def page_executive_overview():
    st.header("Executive Overview")
    st.markdown("High-level summary of business performance, customer retention, and revenue concentration.")
    
    # KPIs
    kpi_query = """
    SELECT 
        COUNT(DISTINCT o.order_id) as total_orders,
        COUNT(DISTINCT c.customer_id) as total_customers,
        SUM(oi.revenue) as total_revenue,
        SUM(oi.quantity) as total_units
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN customers c ON o.customer_id = c.customer_id
    """
    kpis = load_data(kpi_query)
    total_orders = kpis['total_orders'].iloc[0]
    total_customers = kpis['total_customers'].iloc[0]
    total_revenue = kpis['total_revenue'].iloc[0]
    total_units = kpis['total_units'].iloc[0]
    aov = total_revenue / total_orders if total_orders else 0
    
    # Repeat Customer Rate
    repeat_query = """
    WITH customer_orders AS (
        SELECT customer_id, COUNT(DISTINCT order_id) as order_count
        FROM orders
        GROUP BY customer_id
    )
    SELECT 
        COUNT(CASE WHEN order_count > 1 THEN 1 END) as repeat_customers,
        COUNT(*) as all_customers
    FROM customer_orders
    """
    repeat_data = load_data(repeat_query)
    repeat_customers = repeat_data['repeat_customers'].iloc[0]
    all_customers = repeat_data['all_customers'].iloc[0]
    repeat_rate = (repeat_customers / all_customers * 100) if all_customers else 0
    
    st.markdown("---")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Revenue", format_currency(total_revenue))
    col2.metric("Total Orders", format_number(total_orders))
    col3.metric("Avg Order Value", format_currency(aov))
    col4.metric("Unique Customers", format_number(total_customers))
    col5.metric("Repeat Customer Rate", f"{repeat_rate:.1f}%")
    
    st.markdown("---")
    
    col_charts1, col_charts2 = st.columns(2)
    
    # Monthly Trends
    monthly_query = """
    SELECT 
        strftime('%Y-%m', o.order_date) as month,
        SUM(oi.revenue) as revenue,
        COUNT(DISTINCT o.order_id) as orders
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY month
    ORDER BY month
    """
    monthly_data = load_data(monthly_query)
    
    with col_charts1:
        if not monthly_data.empty:
            fig1 = px.line(monthly_data, x='month', y='revenue', markers=True, title='Monthly Revenue Trend', template="plotly_white")
            fig1.update_yaxes(title="", tickprefix="$")
            fig1.update_xaxes(title="")
            fig1.update_layout(height=350, margin=dict(t=40, b=10, l=10, r=10))
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No revenue data available.")
            
    with col_charts2:
        if not monthly_data.empty:
            fig2 = px.bar(monthly_data, x='month', y='orders', title='Monthly Order Volume', color_discrete_sequence=['#ff7f0e'], template="plotly_white")
            fig2.update_yaxes(title="")
            fig2.update_xaxes(title="")
            fig2.update_layout(height=350, margin=dict(t=40, b=10, l=10, r=10))
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No order data available.")
            
    st.markdown("---")
    
    col_charts3, col_charts4 = st.columns(2)
    
    with col_charts3:
        country_query = """
        SELECT 
            shipping_country, 
            SUM(oi.revenue) as revenue
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        GROUP BY shipping_country
        ORDER BY revenue DESC
        LIMIT 10
        """
        country_data = load_data(country_query)
        if not country_data.empty:
            fig3 = px.bar(country_data.sort_values('revenue', ascending=True), x='revenue', y='shipping_country', orientation='h', title='Top 10 Countries by Revenue', template="plotly_white")
            fig3.update_xaxes(title="", tickprefix="$")
            fig3.update_yaxes(title="")
            fig3.update_layout(height=350, margin=dict(t=40, b=10, l=10, r=10))
            st.plotly_chart(fig3, use_container_width=True)
            
    with col_charts4:
        rfm_data = load_rfm_data()
        if not rfm_data.empty:
            segment_revenue = rfm_data.groupby('Segment')['Monetary'].sum().reset_index()
            fig4 = px.pie(segment_revenue, values='Monetary', names='Segment', title='Revenue Contribution by Segment', hole=0.4, template="plotly_white")
            fig4.update_layout(height=350, margin=dict(t=40, b=10, l=10, r=10))
            st.plotly_chart(fig4, use_container_width=True)
            
    st.markdown("---")
    st.subheader("Key Business Takeaways")
    
    if not rfm_data.empty and all_customers > 0:
        champions_revenue = rfm_data[rfm_data['Segment'] == 'Champions']['Monetary'].sum()
        champions_pct = (champions_revenue / total_revenue) * 100 if total_revenue else 0
        champions_count = rfm_data[rfm_data['Segment'] == 'Champions'].shape[0]
        champions_count_pct = (champions_count / all_customers) * 100
        
        at_risk_count = rfm_data[rfm_data['Segment'].isin(['At Risk', 'Hibernating'])].shape[0]
        at_risk_pct = (at_risk_count / all_customers) * 100
        
        st.info(f"🏆 **Revenue Concentration**: The 'Champions' segment accounts for **{champions_pct:.1f}%** of total revenue despite making up only **{champions_count_pct:.1f}%** of the customer base.")
        st.warning(f"⚠️ **Customer Retention**: **{at_risk_pct:.1f}%** of customers fall into the 'At Risk' or 'Hibernating' segments, indicating a significant portion of past buyers have not returned recently.")
        st.success(f"🔄 **Repeat Business**: The repeat customer rate is **{repeat_rate:.1f}%**. Repeat customers are the primary engine of sustained revenue for the business.")
        
def page_customer_intelligence():
    st.title("Customer Intelligence")
    st.markdown("Analyze customer segments using Recency, Frequency, and Monetary (RFM) modeling.")
    
    rfm_data = load_rfm_data()
    
    if rfm_data.empty:
        st.warning("RFM Data is empty or missing.")
        return
        
    st.markdown("### Segment Distribution")
    
    # Aggregates
    segment_agg = rfm_data.groupby('Segment').agg(
        customers=('CustomerID', 'count'),
        revenue=('Monetary', 'sum'),
        avg_monetary=('Monetary', 'mean'),
        avg_recency=('Recency', 'mean'),
        avg_frequency=('Frequency', 'mean')
    ).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.bar(segment_agg, x='customers', y='Segment', orientation='h', title='Customers per Segment', template="plotly_white")
        fig1.update_yaxes(categoryorder='total ascending', title="")
        fig1.update_xaxes(title="Customers")
        fig1.update_layout(height=350, margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        fig2 = px.bar(segment_agg, x='revenue', y='Segment', orientation='h', title='Total Revenue per Segment', color_discrete_sequence=['#2ca02c'], template="plotly_white")
        fig2.update_xaxes(tickprefix="$", title="Revenue")
        fig2.update_yaxes(categoryorder='total ascending', title="")
        fig2.update_layout(height=350, margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig2, use_container_width=True)
        
    st.markdown("### Segment Metrics Table")
    formatted_agg = segment_agg.copy()
    formatted_agg['revenue'] = formatted_agg['revenue'].apply(format_currency)
    formatted_agg['avg_monetary'] = formatted_agg['avg_monetary'].apply(format_currency)
    formatted_agg['avg_recency'] = formatted_agg['avg_recency'].apply(lambda x: f"{x:.0f} days")
    formatted_agg['avg_frequency'] = formatted_agg['avg_frequency'].apply(lambda x: f"{x:.1f} orders")
    st.dataframe(formatted_agg, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("### Customer Lookup")
    
    search_col1, search_col2 = st.columns([1, 2])
    
    with search_col1:
        cust_id_input = st.text_input("🔍 Enter Customer ID:", placeholder="e.g. 17850")
        
    if cust_id_input:
        try:
            cust_id = int(cust_id_input)
            cust_rfm = rfm_data[rfm_data['CustomerID'] == cust_id]
            
            if not cust_rfm.empty:
                c_data = cust_rfm.iloc[0]
                
                st.success(f"Customer **{cust_id}** found!")
                
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Current Segment", c_data['Segment'])
                m2.metric("Lifetime Revenue", format_currency(c_data['Monetary']))
                m3.metric("Total Orders", format_number(c_data['Frequency']))
                m4.metric("Days Since Last Order", format_number(c_data['Recency']))
                
                st.markdown("#### Purchase History")
                # Fetch purchase history
                history_query = f"""
                SELECT 
                    o.order_date as 'Date',
                    o.order_id as 'Order ID',
                    COUNT(oi.product_id) as 'Unique Items',
                    SUM(oi.quantity) as 'Total Items',
                    SUM(oi.revenue) as 'Order Revenue'
                FROM orders o
                JOIN order_items oi ON o.order_id = oi.order_id
                WHERE o.customer_id = {cust_id}
                GROUP BY o.order_id, o.order_date
                ORDER BY o.order_date DESC
                """
                history_data = load_data(history_query)
                
                if not history_data.empty:
                    st.dataframe(
                        history_data.style.format({
                            'Order Revenue': format_currency,
                            'Total Items': format_number
                        }),
                        use_container_width=True, 
                        hide_index=True
                    )
                else:
                    st.info("No detailed purchase history found for this customer.")
                
            else:
                st.warning(f"Customer ID **{cust_id}** not found in the dataset.")
        except ValueError:
            st.error("Please enter a valid numeric Customer ID.")
    else:
        st.info("Enter a Customer ID to view their lifetime metrics and purchase history.")

def page_product_analytics():
    st.header("Product & Business Analytics")
    st.markdown("Understand product performance, top sellers by revenue and volume, and pricing metrics.")
    
    # Prominent Top-N selector
    top_n = st.radio(
        "Select Top-N Products to Display", 
        options=[10, 20, 50], 
        index=0, 
        horizontal=True
    )
    
    product_query = f"""
    SELECT 
        p.product_name as 'Product Name',
        SUM(oi.revenue) as 'Total Revenue',
        SUM(oi.quantity) as 'Total Quantity',
        COUNT(DISTINCT oi.order_id) as 'Total Orders',
        AVG(oi.unit_price) as 'Avg Price'
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.product_id, p.product_name
    ORDER BY "Total Revenue" DESC
    LIMIT {top_n}
    """
    
    product_data = load_data(product_query)
    
    if product_data.empty:
        st.warning("No product data available.")
        return
        
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        fig = px.bar(product_data.head(10).sort_values('Total Revenue', ascending=True), 
                     x='Total Revenue', y='Product Name', orientation='h', 
                     title='Top 10 Products by Revenue', template="plotly_white")
        fig.update_yaxes(title="")
        fig.update_xaxes(tickprefix="$", title="")
        fig.update_layout(height=400, margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)
        
    with col_chart2:
        qty_query = f"""
        SELECT 
            p.product_name as 'Product Name',
            SUM(oi.quantity) as 'Total Quantity'
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY "Total Quantity" DESC
        LIMIT 10
        """
        qty_data = load_data(qty_query)
        if not qty_data.empty:
            fig_qty = px.bar(qty_data.sort_values('Total Quantity', ascending=True), 
                             x='Total Quantity', y='Product Name', orientation='h', 
                             color_discrete_sequence=['#9467bd'], title='Top 10 Products by Volume', template="plotly_white")
            fig_qty.update_yaxes(title="")
            fig_qty.update_xaxes(title="")
            fig_qty.update_layout(height=400, margin=dict(t=40, b=10, l=10, r=10))
            st.plotly_chart(fig_qty, use_container_width=True)
    
    st.markdown("---")
    st.subheader(f"Product Performance Metrics (Top {top_n})")
    
    # Format table for cleaner display
    st.dataframe(
        product_data.style.format({
            'Total Revenue': format_currency,
            'Avg Price': format_currency,
            'Total Quantity': format_number,
            'Total Orders': format_number
        }), 
        use_container_width=True, 
        hide_index=True
    )
    


def page_retention():
    st.header("Retention & Customer Behavior")
    st.markdown("Examine purchasing frequencies, recency, and monthly engagement trends.")
    
    rfm_data = load_rfm_data()
    
    col1, col2, col3 = st.columns(3)
    
    # Calculate returning vs one time
    frequency_counts = rfm_data['Frequency'].value_counts()
    one_time = frequency_counts.get(1, 0)
    returning = rfm_data[rfm_data['Frequency'] > 1].shape[0]
    total = rfm_data.shape[0]
    
    col1.metric("One-Time Customers", format_number(one_time))
    col2.metric("Returning Customers", format_number(returning))
    col3.metric("Repeat Purchase Rate", f"{(returning/total*100):.1f}%" if total else "0%")
    
    st.markdown("---")
    
    col_charts1, col_charts2 = st.columns(2)
    
    with col_charts1:
        st.subheader("Customer Recency Distribution")
        fig = px.histogram(rfm_data, x="Recency", nbins=50, title="Days Since Last Purchase", template="plotly_white")
        fig.update_xaxes(title="Days")
        fig.update_yaxes(title="Customers")
        fig.update_layout(height=350, margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)
    
    with col_charts2:
        st.subheader("Monthly Active Customers (MAC)")
        mac_query = """
        SELECT 
            strftime('%Y-%m', order_date) as month,
            COUNT(DISTINCT customer_id) as active_customers
        FROM orders
        GROUP BY month
        ORDER BY month
        """
        mac_data = load_data(mac_query)
        if not mac_data.empty:
            fig_mac = px.line(mac_data, x='month', y='active_customers', markers=True, title="Unique Customers per Month", template="plotly_white")
            fig_mac.update_xaxes(title="")
            fig_mac.update_yaxes(title="Active Customers")
            fig_mac.update_layout(height=350, margin=dict(t=40, b=10, l=10, r=10))
            st.plotly_chart(fig_mac, use_container_width=True)
        
    st.markdown("---")
    st.subheader("Retention Insights")
    st.info("💡 **Repeat Purchasers**: Returning customers are highly valuable, typically spending significantly more than one-time buyers over their lifetime.")
    st.warning("📉 **Recency Tail**: The histogram shows a long tail of customers who haven't purchased in over 100 days. These correspond to the **'At Risk'** and **'Hibernating'** segments.")
    st.success("📈 **Monthly Activity**: Monthly active customers highlight the seasonal engagement of the user base, typically peaking during holiday months like November.")

def page_sql_analytics():
    st.header("SQL Analytics")
    st.markdown("Demonstrating live SQL execution against the embedded SQLite database (`ecommerce.db`).")
    
    queries = {
        "Monthly Revenue": """SELECT 
    strftime('%Y-%m', o.order_date) AS order_month,
    ROUND(SUM(oi.revenue), 2) AS monthly_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY order_month
ORDER BY order_month;""",
        "Top 10 Customers": """SELECT 
    c.customer_id, 
    c.country, 
    ROUND(SUM(oi.revenue), 2) AS total_spend
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id
ORDER BY total_spend DESC
LIMIT 10;""",
        "Revenue by Country": """SELECT 
    shipping_country, 
    ROUND(SUM(oi.revenue), 2) AS total_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY shipping_country
ORDER BY total_revenue DESC
LIMIT 10;""",
        "Average Order Value": """SELECT 
    ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM order_items;"""
    }
    
    selected_query_name = st.selectbox("📌 Select a Query to Execute", list(queries.keys()))
    sql_string = queries[selected_query_name]
    
    st.markdown("---")
    
    col_sql, col_result = st.columns([1, 1.2])
    
    with col_sql:
        st.subheader("SQL Query")
        st.code(sql_string, language="sql")
    
    with col_result:
        st.subheader("Execution Result")
        try:
            result_df = load_data(sql_string)
            st.dataframe(result_df, use_container_width=True, hide_index=True)
            
            # Add basic chart if applicable
            if len(result_df.columns) == 2 and len(result_df) > 1:
                x_col, y_col = result_df.columns[0], result_df.columns[1]
                if pd.api.types.is_numeric_dtype(result_df[y_col]):
                    fig = px.bar(result_df, x=x_col, y=y_col, title=selected_query_name, template="plotly_white")
                    fig.update_layout(height=300, margin=dict(t=40, b=10, l=10, r=10))
                    st.plotly_chart(fig, use_container_width=True)
                    
        except Exception as e:
            st.error(f"Error executing query: {str(e)}")

# --- 6. ROUTING ---
if selected_page == "Executive Overview":
    page_executive_overview()
elif selected_page == "Customer Intelligence":
    page_customer_intelligence()
elif selected_page == "Product & Business Analytics":
    page_product_analytics()
elif selected_page == "Retention & Customer Behavior":
    page_retention()
elif selected_page == "SQL Analytics":
    page_sql_analytics()
