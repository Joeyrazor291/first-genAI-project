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
# Secrets are stored in .streamlit/secrets.toml (local) or app settings (Streamlit Cloud)
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
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .restaurant-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
        background-color: #f9f9f9;
    }
    .rating-badge {
        display: inline-block;
        background-color: #ffc107;
        color: black;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    .price-badge {
        display: inline-block;
        background-color: #28a745;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        margin-left: 8px;
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
    st.title("🍽️ Restaurant Recommendation Engine")
    st.markdown("Find your perfect restaurant based on your preferences")
    
    # Sidebar - Statistics and Info
    with st.sidebar:
        st.header("📊 Database Info")
        engine = load_engine()
        
        if engine is None:
            st.error("Could not load recommendation engine. Please check your configuration.")
        else:
            try:
                stats = engine.get_database_stats()
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Restaurants", stats.get("total_restaurants", 0))
                    st.metric("Cuisines", stats.get("total_cuisines", 0))
                with col2:
                    st.metric("Locations", stats.get("total_locations", 0))
                    st.metric("Avg Rating", f"{stats.get('avg_rating', 0):.2f}")
                
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
    st.subheader("🔍 Find Restaurants")
    
    # Get available options
    cuisines, locations = get_available_options()
    
    # Create form
    with st.form("preference_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            cuisine = st.multiselect(
                "Cuisine Type",
                options=sorted(cuisines),
                default=None,
                help="Select one or more cuisines"
            )
            
            min_rating = st.slider(
                "Minimum Rating",
                min_value=0.0,
                max_value=5.0,
                value=3.5,
                step=0.1
            )
        
        with col2:
            location = st.multiselect(
                "Location",
                options=sorted(locations),
                default=None,
                help="Select one or more locations"
            )
            
            max_price = st.slider(
                "Maximum Price",
                min_value=0,
                max_value=5,
                value=5,
                step=1,
                help="Price range: 1 (cheap) to 5 (expensive)"
            )
        
        limit = st.number_input(
            "Number of Recommendations",
            min_value=1,
            max_value=50,
            value=5,
            step=1
        )
        
        submitted = st.form_submit_button("🔍 Get Recommendations", use_container_width=True)
    
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
                st.info(f"📋 Filters Applied: {filter_summary}")
                
                # Display results
                st.subheader(f"✨ Found {len(recommendations)} Recommendations")
                
                for idx, restaurant in enumerate(recommendations, 1):
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"### {idx}. {restaurant.get('name', 'N/A')}")
                            
                            # Restaurant details
                            details = []
                            if restaurant.get('cuisine'):
                                details.append(f"🍜 {restaurant['cuisine']}")
                            if restaurant.get('location'):
                                details.append(f"📍 {restaurant['location']}")
                            if details:
                                st.markdown(" | ".join(details))
                        
                        with col2:
                            rating = restaurant.get('rating', 0)
                            price = restaurant.get('price', 0)
                            st.markdown(f"⭐ {rating:.1f} | 💰 {'$' * price}")
                        
                        # Description
                        if restaurant.get('description'):
                            st.markdown(f"*{restaurant['description']}*")
                        
                        # AI Explanation
                        if restaurant.get('explanation'):
                            with st.expander("💡 AI Explanation"):
                                st.markdown(restaurant['explanation'])
                        
                        st.divider()
        
        except Exception as e:
            st.error(f"Error getting recommendations: {str(e)}")
            st.write("Debug info:", str(e))

if __name__ == "__main__":
    main()
