import streamlit as st
import sys
import os
from pathlib import Path

# Add phase directories to path
phase_dirs = [
    "restaurant-recommendation/phase-1-data-pipeline",
    "restaurant-recommendation/phase-3-preference-processing",
    "restaurant-recommendation/phase-4-llm-integration",
    "restaurant-recommendation/phase-5-recommendation-engine",
]

for phase_dir in phase_dirs:
    sys.path.insert(0, str(Path(phase_dir) / "src"))

# Load environment variables from .env files (only if dotenv is available)
try:
    from dotenv import load_dotenv
    for phase_dir in phase_dirs:
        env_path = Path(phase_dir) / ".env"
        if env_path.exists():
            load_dotenv(env_path)
except ImportError:
    # dotenv not available (e.g., on Streamlit Cloud), skip .env loading
    pass

# Load Streamlit secrets (for local development and Streamlit Cloud)
try:
    llm_provider = st.secrets.get("llm_provider", "groq")
    if llm_provider == "groq":
        groq_key = st.secrets.get("groq_api_key", "")
        if groq_key:
            os.environ["GROQ_API_KEY"] = groq_key
    elif llm_provider == "openrouter":
        openrouter_key = st.secrets.get("openrouter_api_key", "")
        if openrouter_key:
            os.environ["OPENROUTER_API_KEY"] = openrouter_key
    os.environ["LLM_PROVIDER"] = llm_provider
except Exception as e:
    # Secrets not available, will use environment variables
    pass

from recommendation_engine import RecommendationEngine
from preference_processor import PreferenceProcessor

# Page configuration
st.set_page_config(
    page_title="Restaurant Recommendation Engine",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Main container */
    .main {
        padding: 0;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px 20px;
        border-radius: 0;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .header-title {
        font-size: 2.5em;
        font-weight: bold;
        margin: 0;
        color: white;
    }
    
    .header-subtitle {
        font-size: 1.1em;
        color: rgba(255,255,255,0.9);
        margin-top: 10px;
    }
    
    /* Form container */
    .form-container {
        background: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }
    
    /* Section title */
    .section-title {
        font-size: 1.3em;
        font-weight: bold;
        color: #333;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Cuisine grid */
    .cuisine-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
        gap: 15px;
        margin-bottom: 20px;
    }
    
    .cuisine-item {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .cuisine-item:hover {
        border-color: #667eea;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }
    
    .cuisine-item.selected {
        background: #667eea;
        color: white;
        border-color: #667eea;
    }
    
    .cuisine-icon {
        font-size: 2em;
        margin-bottom: 8px;
    }
    
    .cuisine-name {
        font-size: 0.9em;
        font-weight: 500;
    }
    
    /* Restaurant card */
    .restaurant-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .restaurant-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    .restaurant-header {
        display: flex;
        justify-content: space-between;
        align-items: start;
        margin-bottom: 12px;
    }
    
    .restaurant-name {
        font-size: 1.2em;
        font-weight: bold;
        color: #333;
    }
    
    .restaurant-rating {
        background: #ffc107;
        color: black;
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9em;
    }
    
    .restaurant-details {
        display: flex;
        gap: 20px;
        margin-bottom: 12px;
        font-size: 0.95em;
        color: #666;
    }
    
    .restaurant-detail-item {
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .restaurant-description {
        color: #666;
        font-size: 0.95em;
        margin-bottom: 12px;
        line-height: 1.5;
    }
    
    .explanation-box {
        background: #f0f4ff;
        border-left: 4px solid #667eea;
        padding: 12px;
        border-radius: 4px;
        font-size: 0.9em;
        color: #333;
        line-height: 1.5;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1em;
        cursor: pointer;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Slider styling */
    .stSlider {
        margin-bottom: 20px;
    }
    
    /* Selectbox styling */
    .stSelectbox, .stMultiSelect {
        margin-bottom: 15px;
    }
    
    /* Results section */
    .results-header {
        font-size: 1.5em;
        font-weight: bold;
        color: #333;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #667eea;
    }
    
    /* Filter summary */
    .filter-summary {
        background: #e8f0fe;
        border-left: 4px solid #667eea;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        color: #333;
    }
    
    /* No results message */
    .no-results {
        text-align: center;
        padding: 40px;
        color: #999;
    }
    
    /* Sidebar */
    .sidebar-content {
        padding: 20px;
    }
    
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        text-align: center;
    }
    
    .stat-number {
        font-size: 1.8em;
        font-weight: bold;
    }
    
    .stat-label {
        font-size: 0.9em;
        opacity: 0.9;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_engine():
    """Load recommendation engine once"""
    try:
        return RecommendationEngine()
    except Exception as e:
        st.error(f"Error loading recommendation engine: {str(e)}")
        return None

@st.cache_data
def get_available_options():
    """Get available cuisines and locations"""
    engine = load_engine()
    if engine is None:
        return [], []
    try:
        cuisines = engine.get_available_cuisines()
        locations = engine.get_available_locations()
        return cuisines, locations
    except Exception as e:
        st.error(f"Error loading options: {str(e)}")
        return [], []

def main():
    # Header
    st.markdown("""
        <div class="header-container">
            <h1 class="header-title">🍽️ Restaurant Recommendation Engine</h1>
            <p class="header-subtitle">Find your perfect restaurant based on your preferences</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar - Statistics and Info
    with st.sidebar:
        st.header("📊 Database Info")
        engine = load_engine()
        
        if engine is None:
            st.error("Could not load recommendation engine. Please check your configuration.")
        else:
            try:
                stats = engine.get_database_stats()
                
                # Display stats in boxes
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                        <div class="stat-box">
                            <div class="stat-number">{stats.get('total_restaurants', 0):,}</div>
                            <div class="stat-label">Restaurants</div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class="stat-box">
                            <div class="stat-number">{stats.get('total_cuisines', 0)}</div>
                            <div class="stat-label">Cuisines</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                        <div class="stat-box">
                            <div class="stat-number">{stats.get('total_locations', 0)}</div>
                            <div class="stat-label">Locations</div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class="stat-box">
                            <div class="stat-number">{stats.get('avg_rating', 0):.1f}⭐</div>
                            <div class="stat-label">Avg Rating</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.divider()
                st.subheader("ℹ️ About")
                st.info("""
                This recommendation engine uses:
                - **Database**: SQLite with 9,216+ restaurants
                - **AI**: LLM-powered explanations
                - **Filtering**: Smart preference matching
                """)
                
                # Health check
                st.subheader("🔍 Status")
                st.success("✅ Database Connected")
                
            except Exception as e:
                st.error(f"Error loading stats: {str(e)}")
    
    # Main content
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">🔍 Find Restaurants</div>', unsafe_allow_html=True)
    
    # Get available options
    cuisines, locations = get_available_options()
    
    # Create form
    with st.form("preference_form"):
        # Location section
        st.markdown('<div class="section-title">📍 Location in Bengaluru</div>', unsafe_allow_html=True)
        location = st.multiselect(
            "Select Location",
            options=sorted(locations),
            default=None,
            help="Select one or more locations",
            label_visibility="collapsed"
        )
        
        # Cuisine section
        st.markdown('<div class="section-title">🍜 Cuisines</div>', unsafe_allow_html=True)
        st.markdown("Type to search cuisines...")
        cuisine = st.multiselect(
            "Select Cuisine",
            options=sorted(cuisines),
            default=None,
            help="Select one or more cuisines",
            label_visibility="collapsed"
        )
        
        # Filters section
        st.markdown('<div class="section-title">⚙️ Filters</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            min_rating = st.slider(
                "Minimum Rating",
                min_value=0.0,
                max_value=5.0,
                value=3.5,
                step=0.1
            )
        
        with col2:
            max_price = st.slider(
                "Maximum Price",
                min_value=0,
                max_value=5,
                value=5,
                step=1,
                help="Price range: 1 (cheap) to 5 (expensive)"
            )
        
        with col3:
            limit = st.number_input(
                "Number of Recommendations",
                min_value=1,
                max_value=50,
                value=5,
                step=1
            )
        
        submitted = st.form_submit_button("🔍 Get Recommendations", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process recommendations
    if submitted:
        if not cuisine and not location:
            st.warning("Please select at least one cuisine or location")
            return
        
        try:
            with st.spinner("🔄 Finding perfect restaurants..."):
                # Prepare preferences
                preferences = {
                    "cuisine": cuisine if cuisine else None,
                    "location": location if location else None,
                    "min_rating": min_rating,
                    "max_price": max_price,
                    "limit": limit
                }
                
                # Validate preferences using PreferenceProcessor
                processor = PreferenceProcessor()
                validation_result = processor.validate_and_normalize(preferences)
                
                if not validation_result.is_valid:
                    st.error(f"Invalid preferences: {', '.join(validation_result.errors)}")
                    return
                
                validated_prefs = validation_result.normalized_preferences
                
                # Get recommendations
                engine = load_engine()
                if engine is None:
                    st.error("Could not load recommendation engine. Please check your configuration.")
                    return
                
                recommendations = engine.get_recommendations(validated_prefs)
                
                if not recommendations:
                    st.warning("No restaurants found matching your preferences. Try adjusting your filters.")
                    return
                
                # Display filter summary
                filter_summary = processor.get_filter_summary(validated_prefs)
                st.markdown(f'<div class="filter-summary">📋 Filters Applied: {filter_summary}</div>', unsafe_allow_html=True)
                
                # Display results
                st.markdown(f'<div class="results-header">✨ Found {len(recommendations)} Recommendations</div>', unsafe_allow_html=True)
                
                for idx, restaurant in enumerate(recommendations, 1):
                    # Restaurant card
                    rating = restaurant.get('rating', 0)
                    price = restaurant.get('price', 0)
                    
                    card_html = f"""
                    <div class="restaurant-card">
                        <div class="restaurant-header">
                            <div>
                                <div class="restaurant-name">{idx}. {restaurant.get('name', 'N/A')}</div>
                            </div>
                            <div class="restaurant-rating">⭐ {rating:.1f}</div>
                        </div>
                        <div class="restaurant-details">
                            <div class="restaurant-detail-item">🍜 {restaurant.get('cuisine', 'N/A')}</div>
                            <div class="restaurant-detail-item">📍 {restaurant.get('location', 'N/A')}</div>
                            <div class="restaurant-detail-item">💰 {'₹' * price}</div>
                        </div>
                    """
                    
                    if restaurant.get('description'):
                        card_html += f'<div class="restaurant-description">{restaurant["description"]}</div>'
                    
                    if restaurant.get('explanation'):
                        card_html += f'<div class="explanation-box"><strong>💡 Why this restaurant:</strong><br>{restaurant["explanation"]}</div>'
                    
                    card_html += '</div>'
                    
                    st.markdown(card_html, unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"Error getting recommendations: {str(e)}")

if __name__ == "__main__":
    main()
