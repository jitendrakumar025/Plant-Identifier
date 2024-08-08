import streamlit as st
from PIL import Image
from gemini_api import identify_plant
import json

st.set_page_config(page_title="Plant Identifier", page_icon="🌿", layout="wide")
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">', unsafe_allow_html=True)


st.markdown("""
<style>
.footer {
    position: sticky;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #4CAF50;
    color: white;
    text-align: center;
    padding: 10px 0;
}
.plant-info {
    background-color: white;
    border-radius: 10px;
    padding: 20px;
    margin-top: 5.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.plant-info h3 {
    color: #4CAF50;
    border-bottom: 2px solid #4CAF50;
    padding-bottom: 10px;
    margin-bottom: 20px;
}
.plant-info table {
    width: 100%;
    border-collapse: collapse;
}
.plant-info th, .plant-info td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}
.plant-info th {
    background-color: #f2f2f2;
    color: #4CAF50;
}
.plant-info td {
    color: black;
}
.plant-info p {
    color: black;
    margin-top: 20px;
}
.step-box {
    background-color: #1e2761;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    text-align: center;
}
.step-icon {
    background-color: #a7ff83;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0 auto 1rem auto;
}
.step-icon i {
    color: #1e2761;
    font-size: 24px;
}
.step-title {
    color: white;
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}
.step-description {
    color: #a0a0a0;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

if 'camera_active' not in st.session_state:
    st.session_state.camera_active = False


def main():
    st.title("🌿 Plant Identifier")
    st.write(
        "Discover the world of plants! Upload an image or use your camera to identify plants.")
    st.subheader("Get Plant Image")
    col3, col4 = st.columns([2, 1])
    image = None
    with col3:
        uploaded_file = st.file_uploader(
            "Upload an image of a plant", type=["jpg", "jpeg", "png"])

    with col4:
        if st.button("Or Take a Picture"):
            st.session_state.camera_active = True

            if st.session_state.camera_active:
                camera_image = st.camera_input('Camera',label_visibility='hidden')
                if camera_image is not None:
                    image = Image.open(camera_image)
                    st.session_state.camera_active = False

            if uploaded_file is not None:
                image = Image.open(uploaded_file)

    col1, col2 = st.columns([1, 1])
    with col1:
        if image is not None:
            st.image(image, caption="Plant Image", use_column_width=True)

            if st.button("Identify Plant"):
                with st.spinner("Identifying plant..."):
                    response_text = identify_plant(image)
                    try:
                        plant_info = json.loads(response_text)
                        with col2:
                            st.markdown("""
                                    <div class="plant-info">
                                        <h3>Plant Information</h3>
                                        <table>
                                            <tr><th>Attribute</th><th>Value</th></tr>
                                            <tr><td>Name</td><td>{}</td></tr>
                                            <tr><td>Scientific Name</td><td>{}</td></tr>
                                            <tr><td>Family</td><td>{}</td></tr>
                                            <tr><td>Native Region</td><td>{}</td></tr>
                                            <tr><td>Growth Habit</td><td>{}</td></tr>
                                            <tr><td>Flower Color</td><td>{}</td></tr>
                                            <tr><td>Leaf Type</td><td>{}</td></tr>
                                        </table>
                                        <h3>Description</h3>
                                        <p>{}</p>
                                    </div>
                                    """.format(
                                plant_info.get('name', 'N/A'),
                                plant_info.get('scientificName', 'N/A'),
                                plant_info.get('family', 'N/A'),
                                plant_info.get('nativeRegion', 'N/A'),
                                plant_info.get('growthHabit', 'N/A'),
                                plant_info.get('flowerColor', 'N/A'),
                                plant_info.get('leafType', 'N/A'),
                                plant_info.get(
                                    'description', 'No description available.')
                            ), unsafe_allow_html=True)

                    except json.JSONDecodeError:
                        st.error(
                            "Failed to parse JSON response. Here's the raw text:")
                        st.text(response_text)

    st.markdown("<h2 style='text-align: center; color: white;'>How It Works</h2>",
                unsafe_allow_html=True)
    colA, colB, colC = st.columns([1, 1, 1])

    with colA:
        st.markdown("""<div class="step-box">
            <div class="step-icon">
                <i class="fas fa-upload"></i>
            </div>
            <div class="step-title">Upload Image</div>
            <div class="step-description">Take a photo or upload an existing image of a plant you want to identify.</div>
        </div>""", unsafe_allow_html=True)

    with colB:
        st.markdown("""<div class="step-box">
            <div class="step-icon">
                <i class="fas fa-robot"></i>
            </div>
            <div class="step-title">AI Analysis</div>
            <div class="step-description">Our advanced AI analyzes the image to identify the plant species.</div>
        </div>""", unsafe_allow_html=True)

    with colC:
        st.markdown("""<div class="step-box">
            <div class="step-icon">
                <i class="fas fa-info-circle"></i>
            </div>
            <div class="step-title">Get Information</div>
            <div class="step-description">Receive detailed information about the plant, including its name, scientific name, and characteristics.</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("About Plant Identification")
    st.write("""
        Plant identification is a fascinating process that combines botany, technology, and a keen eye for detail. 
        Our AI-powered tool uses advanced image recognition to analyze the unique features of plants, including:
        
        - Leaf shape and arrangement
        - Flower structure and color
        - Stem characteristics
        - Overall plant habit
        
        By uploading a clear image of a plant, you can quickly get information about its identity, characteristics, and interesting facts.
        This can be helpful for gardeners, nature enthusiasts, students, and anyone curious about the plants around them.
        """)

    st.sidebar.title("Plant Identification Tips")
    st.sidebar.write("""
        To get the best results:
        1. Use a clear, well-lit image
        2. Focus on distinctive features (flowers, leaves, etc.)
        3. Include multiple parts of the plant if possible
        4. Avoid blurry or dark images
        """)
    st.markdown("""
        <div class="footer">
            <p>© 2024 Plant Identifier. All rights reserved.| Powered by AI</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
