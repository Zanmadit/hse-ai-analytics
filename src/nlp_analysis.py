import sys
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.config import settings

model = SentenceTransformer(settings.EMBED_MODEL)

def cluster_incidents(texts, n_clusters=settings.NUMBER_CLUSTERS):
    '''
    Uses machine learning methods (SBERT embeddings and K-means) to perform semantic analysis of textual incident descriptions. 
    Automatically groups incidents by underlying causes (e.g., “electrical safety” or “fall from height”), 
    which are difficult to identify through manual coding.
    '''
    
    embeddings = model.encode(texts)

    kmeans = KMeans(n_clusters=n_clusters)
    labels = kmeans.fit_predict(embeddings)

    return labels