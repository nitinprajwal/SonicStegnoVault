import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import librosa
import numpy as np
import pandas as pd
from PIL import Image
import io
import base64
from pathlib import Path
from datetime import datetime
import os
import json

from encryption.key_generation import generate_keys
from encryption.encrypt_audio import encrypt_audio
from encryption.decrypt_audio import decrypt_audio
from steganography.embed_audio import embed_data_into_image
from steganography.extract_audio import extract_data_from_image
from utils.metrics import calculate_psnr, calculate_mse, calculate_embedding_capacity
from utils.audio_processing import get_audio_features
from utils.visualization import create_waveform_plot, create_spectrogram_plot, create_mel_spectrogram, create_chroma_plot, create_spectral_features_plot
from utils.audio_processing import get_audio_statistics

# Page configuration
st.set_page_config(
    page_title="StegoCrypt Audio by Nitin Prajwal R",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
# Enhanced Custom CSS with branding
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    .css-1d391kg {
        background-color: #1E2329;
    }
    .stButton>button {
        background-color: #2E7D32;
        color: white;
    }
    .metric-card {
        background-color: #1E2329;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem;
    }
    .author-banner {
        background-color: #1E2329;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
        border: 1px solid #2E7D32;
    }
    .social-links {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
    }
    .copyright-text {
        font-size: 0.8rem;
        opacity: 0.8;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Author Banner
st.markdown("""
<div class="author-banner">
    <h2>StegoCrypt Audio</h2>
    <h4>Created by Nitin Prajwal R</h4>
    <div class="social-links">
        <a href="https://github.com/nitinprajwal" target="_blank">
            <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" />
        </a>
        <a href="https://www.linkedin.com/in/nitinprajwal/" target="_blank">
            <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />
        </a>
        <a href="https://x.com/nitinprajwalr" target="_blank">
            <img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" />
        </a>
    </div>
    <p class="copyright-text">
        © 2024 Nitin Prajwal R. All rights reserved. This application is protected under international copyright laws.
        Unauthorized reproduction or distribution is strictly prohibited.
    </p>
</div>
""", unsafe_allow_html=True)

def add_watermark(fig):
    """Add watermark to Plotly figures"""
    fig.add_annotation(
        text=f"© {datetime.now().year} Nitin Prajwal R | github.com/nitinprajwal",
        x=0.97,
        y=0.03,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=10, color="gray"),
        opacity=0.7,
        align="right"
    )
    return fig

def create_visualization(y, sr, plot_type):
    if plot_type == "waveform":
        fig = create_waveform_plot(y, sr)
    elif plot_type == "spectrogram":
        fig = create_spectrogram_plot(y, sr)
    elif plot_type == "mel":
        fig = create_mel_spectrogram(y, sr)
    elif plot_type == "chroma":
        fig = create_chroma_plot(y, sr)
    elif plot_type == "spectral":
        fig = create_spectral_features_plot(y, sr)
    
    return add_watermark(fig)

def main():
    st.title("🎵 StegoCrypt Audio")
    st.markdown("### Advanced Audio Steganography with Hybrid Encryption")

    # Sidebar
    st.sidebar.title("Navigation")
    mode = st.sidebar.radio("Select Mode", ["Embedding", "Extraction"])

    if mode == "Embedding":
        embedding_process()
    else:
        extraction_process()

def embedding_process():
    st.header("📥 Embedding Process")
    
    # File uploads
    audio_file = st.file_uploader("Upload Audio File", type=['wav'])
    carrier_image = st.file_uploader("Upload Carrier Image", type=['png', 'jpg', 'jpeg'])

    if audio_file and carrier_image:
        # Read files
        audio_bytes = audio_file.read()
        image = Image.open(carrier_image)

        # Display original files
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Audio Analysis")
            y, sr = librosa.load(io.BytesIO(audio_bytes))
            
            # Update visualization calls to include watermark
            waveform_plot = create_visualization(y, sr, "waveform")
            st.plotly_chart(waveform_plot, use_container_width=True)
    
            spectrogram_plot = create_visualization(y, sr, "spectrogram")
            st.plotly_chart(spectrogram_plot, use_container_width=True)
    
            mel_plot = create_visualization(y, sr, "mel")
            st.plotly_chart(mel_plot, use_container_width=True)


        with col2:
            st.subheader("Carrier Image")
            st.image(image, use_column_width=True)
            
            # Image histograms
            fig = px.histogram(np.array(image).ravel(), 
                             title="Image Pixel Distribution",
                             labels={'value': 'Pixel Value', 'count': 'Frequency'})
            st.plotly_chart(fig, use_container_width=True)

        if st.button("Embed Audio"):
            with st.spinner("Processing..."):
                # Generate keys
                generate_keys()
                
                # Encrypt and embed
                encrypted_aes_key, nonce, tag, ciphertext = encrypt_audio(audio_bytes)
                output_path = "stego_image.png"
                embed_data_into_image(carrier_image, 
                                    (encrypted_aes_key, nonce, tag, ciphertext),
                                    output_path)

                # Calculate metrics
                stego_image = Image.open(output_path)
                psnr = calculate_psnr(np.array(image), np.array(stego_image))
                mse = calculate_mse(np.array(image), np.array(stego_image))
                capacity = calculate_embedding_capacity(np.array(image))

                # Display results
                st.success("Audio successfully embedded!")
                
                # Metrics display
                metrics_cols = st.columns(3)
                with metrics_cols[0]:
                    st.metric("PSNR", f"{psnr:.2f} dB")
                with metrics_cols[1]:
                    st.metric("MSE", f"{mse:.6f}")
                with metrics_cols[2]:
                    st.metric("Embedding Capacity", f"{capacity/1024:.2f} KB")

                # Download section
                st.subheader("Download Files")
                download_cols = st.columns(3)
                
                with download_cols[0]:
                    with open("stego_image.png", "rb") as file:
                        btn = st.download_button(
                            label="Download Stego Image",
                            data=file,
                            file_name="stego_image.png",
                            mime="image/png"
                        )
                
                with download_cols[1]:
                    with open("public.pem", "rb") as file:
                        btn = st.download_button(
                            label="Download Public Key",
                            data=file,
                            file_name="public.pem",
                            mime="application/x-pem-file"
                        )
                
                with download_cols[2]:
                    with open("private.pem", "rb") as file:
                        btn = st.download_button(
                            label="Download Private Key",
                            data=file,
                            file_name="private.pem",
                            mime="application/x-pem-file"
                        )

def show_detailed_analysis(y, sr):
    """Show detailed audio analysis"""
    
    st.subheader("Advanced Audio Analysis")
    
    tabs = st.tabs(["Spectral", "Energy", "Pitch", "Compare"])
    
    with tabs[0]:
        st.plotly_chart(create_spectral_features_plot(y, sr), use_container_width=True)
        
    with tabs[1]:
        st.write("Energy contour plot is not available.")
        
    with tabs[2]:
        st.plotly_chart(create_chroma_plot(y, sr), use_container_width=True)
        
    with tabs[3]:
        if 'original_audio' in st.session_state:
            col1, col2 = st.columns(2)
            with col1:
                st.write("Original Audio")
                st.plotly_chart(create_waveform_plot(
                    st.session_state.original_audio, sr), 
                    use_container_width=True)
            with col2:
                st.write("Processed Audio") 
                st.plotly_chart(create_waveform_plot(y, sr),
                    use_container_width=True)

def extraction_process():
    st.header("📤 Extraction Process")
    
    # File uploads
    stego_image = st.file_uploader("Upload Stego Image", type=['png'])
    private_key = st.file_uploader("Upload Private Key", type=['pem'])

    if stego_image and private_key:
        # Save uploaded files
        with open("stego_image.png", "wb") as f:
            f.write(stego_image.getvalue())
        with open("private.pem", "wb") as f:
            f.write(private_key.getvalue())

        if st.button("Extract Audio"):
            with st.spinner("Extracting audio..."):
                # Extract and decrypt
                extracted_data = extract_data_from_image("stego_image.png")
                decrypted_audio = decrypt_audio(*extracted_data)
                
                # Save decrypted audio
                output_path = "decrypted_audio.wav"
                with open(output_path, "wb") as f:
                    f.write(decrypted_audio)

                # Audio analysis
                y, sr = librosa.load(output_path)
                
                st.success("Audio successfully extracted!")
                
                # Display audio player
                st.audio(output_path)
                
                # Display visualizations
                st.subheader("Extracted Audio Analysis")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(create_waveform_plot(y, sr), use_container_width=True)
                with col2:
                    st.plotly_chart(create_spectrogram_plot(y, sr), use_container_width=True)
                
                # Additional features
                features = get_audio_features(y, sr)
                st.subheader("Audio Features")
                
                # Create a DataFrame for features
                df = pd.DataFrame(features.items(), columns=['Feature', 'Value'])
                st.table(df)
                
                # Download extracted audio
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="Download Extracted Audio",
                        data=file,
                        file_name="extracted_audio.wav",
                        mime="audio/wav"
                    )

def show_extraction_analysis(y, sr):
    """Show extraction analysis results"""
    
    features = get_audio_features(y, sr)
    stats = get_audio_statistics(y)
    
    st.subheader("Extracted Audio Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Audio Features")
        st.json(features)
        
        # Download features
        features_json = json.dumps(features, indent=2)
        st.download_button(
            "Download Features JSON",
            features_json,
            "audio_features.json",
            "application/json"
        )
        
    with col2:
        st.write("Statistical Analysis")
        st.json(stats)
        
        # Download stats
        stats_json = json.dumps(stats, indent=2)
        st.download_button(
            "Download Statistics JSON", 
            stats_json,
            "audio_stats.json",
            "application/json"
        )

if __name__ == "__main__":
    main()