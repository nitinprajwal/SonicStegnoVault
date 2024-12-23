import plotly.graph_objects as go
import numpy as np
import librosa

def create_waveform_plot(y, sr):
    """Create interactive waveform plot"""
    times = np.arange(len(y))/sr
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=y, name='Waveform'))
    fig.update_layout(
        title="Audio Waveform",
        xaxis_title="Time (s)",
        yaxis_title="Amplitude",
        template="plotly_dark"
    )
    return fig

def create_spectrogram_plot(y, sr):
    """Create interactive spectrogram plot"""
    D = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    
    fig = go.Figure(data=go.Heatmap(
        z=S_db,
        x=librosa.times_like(S_db),
        y=librosa.fft_frequencies(sr=sr),
        colorscale='Viridis'
    ))
    
    fig.update_layout(
        title="Spectrogram",
        xaxis_title="Time (s)",
        yaxis_title="Frequency (Hz)",
        template="plotly_dark"
    )
    return fig

def create_mel_spectrogram(y, sr):
    """Create Mel spectrogram plot"""
    mel_spect = librosa.feature.melspectrogram(y=y, sr=sr)
    mel_db = librosa.power_to_db(mel_spect, ref=np.max)
    
    fig = go.Figure(data=go.Heatmap(
        z=mel_db,
        colorscale='Viridis'
    ))
    
    fig.update_layout(
        title="Mel Spectrogram",
        xaxis_title="Time",
        yaxis_title="Mel Frequency",
        template="plotly_dark"
    )
    return fig

def create_spectral_features_plot(y, sr):
    """Create spectral features visualization"""
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
    spec_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    
    times = librosa.times_like(spec_cent)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=spec_cent, name='Spectral Centroid'))
    fig.add_trace(go.Scatter(x=times, y=spec_bw, name='Spectral Bandwidth'))
    fig.add_trace(go.Scatter(x=times, y=spec_rolloff, name='Spectral Rolloff'))
    
    fig.update_layout(
        title="Spectral Features Analysis",
        xaxis_title="Time (s)", 
        yaxis_title="Frequency (Hz)",
        template="plotly_dark"
    )
    return fig

def create_energy_contour_plot(y, sr):
    """Create energy contour visualization"""
    S = np.abs(librosa.stft(y))
    energy = librosa.feature.rms(S=S)[0]
    times = librosa.times_like(energy)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=energy, fill='tozeroy', name='Energy'))
    
    fig.update_layout(
        title="Energy Contour",
        xaxis_title="Time (s)",
        yaxis_title="Energy",
        template="plotly_dark"
    )
    return fig

def create_chroma_plot(y, sr):
    """Create chromagram visualization"""
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    
    fig = go.Figure(data=go.Heatmap(
        z=chroma,
        x=librosa.times_like(chroma),
        y=['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'],
        colorscale='Viridis'
    ))
    
    fig.update_layout(
        title="Chromagram",
        xaxis_title="Time (s)",
        yaxis_title="Pitch Class",
        template="plotly_dark"
    )
    return fig