"""
Sofia Engine - Host Completa com Todas as Ferramentas

Integra:
- XTTS v2 para síntese de voz
- LivePortrait para animação facial
- Viseme Sync para lip sync
- BeautifulSoup/Playwright para web scraping
- PyPDF2 para processamento de documentos
- ChromaDB para RAG temporário por sessão
"""

import asyncio
import json
from typing import Optional, Dict, List, Any
from datetime import datetime
import logging

# Importações de ferramentas
try:
    from xtts_engine_real import XTTSEngine
    from liveportrait_engine_real import LivePortraitEngine
    from viseme_sync import VisemeSyncEngine
except ImportError:
    pass

try:
    from bs4 import BeautifulSoup
    import requests
except ImportError:
    pass

try:
    from playwright.async_api import async_playwright
except ImportError:
    pass

try:
    import PyPDF2
except ImportError:
    pass

try:
    import chromadb
except ImportError:
    pass


logger = logging.getLogger(__name__)


class SofiaEngine:
    """Engine principal de Sofia - Host completa com todas as ferramentas"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Inicializa Sofia com todas as ferramentas
        
        Args:
            config: Dicionário de configuração
        """
        self.config = config or {}
        self.session_id = datetime.now().isoformat()
        
        # Inicializar engines
        self.tts_engine = None
        self.avatar_engine = None
        self.viseme_engine = None
        self.rag_client = None
        
        # Estado da sessão
        self.session_data = {
            "session_id": self.session_id,
            "created_at": datetime.now().isoformat(),
            "tools_used": [],
            "context": {}
        }
        
        logger.info(f"Sofia Engine inicializado - Session: {self.session_id}")
    
    async def initialize_engines(self):
        """Inicializa todos os engines de forma assíncrona"""
        try:
            # TTS Engine
            self.tts_engine = XTTSEngine()
            logger.info("✅ XTTS v2 Engine inicializado")
            
            # Avatar Engine
            self.avatar_engine = LivePortraitEngine()
            logger.info("✅ LivePortrait Engine inicializado")
            
            # Viseme Engine
            self.viseme_engine = VisemeSyncEngine()
            logger.info("✅ Viseme Sync Engine inicializado")
            
            # ChromaDB para RAG temporário
            self.rag_client = chromadb.Client()
            logger.info("✅ ChromaDB inicializado para RAG temporário")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar engines: {e}")
            raise
    
    # ========== FERRAMENTA 1: SÍNTESE DE VOZ ==========
    
    async def synthesize_speech(self, text: str, voice_profile: str = "sofia_corporate") -> Dict:
        """
        Sintetiza fala usando XTTS v2
        
        Args:
            text: Texto para sintetizar
            voice_profile: Perfil de voz
            
        Returns:
            Dict com áudio, metadados, duração
        """
        try:
            if not self.tts_engine:
                raise ValueError("TTS Engine não inicializado")
            
            result = await self.tts_engine.synthesize(text, voice_profile)
            self.session_data["tools_used"].append("tts")
            
            return {
                "status": "success",
                "audio_path": result.get("audio_path"),
                "duration": result.get("duration"),
                "sample_rate": result.get("sample_rate"),
                "text": text,
                "voice_profile": voice_profile
            }
        except Exception as e:
            logger.error(f"Erro em synthesize_speech: {e}")
            return {"status": "error", "message": str(e)}
    
    # ========== FERRAMENTA 2: ANIMAÇÃO FACIAL ==========
    
    async def generate_animation(self, audio_path: str, avatar_image: str) -> Dict:
        """
        Gera animação facial sincronizada com áudio
        
        Args:
            audio_path: Caminho do arquivo de áudio
            avatar_image: Caminho da imagem do avatar
            
        Returns:
            Dict com vídeo, frames, metadados
        """
        try:
            if not self.avatar_engine:
                raise ValueError("Avatar Engine não inicializado")
            
            result = await self.avatar_engine.generate(audio_path, avatar_image)
            self.session_data["tools_used"].append("animation")
            
            return {
                "status": "success",
                "video_path": result.get("video_path"),
                "frames_count": result.get("frames_count"),
                "fps": result.get("fps"),
                "duration": result.get("duration")
            }
        except Exception as e:
            logger.error(f"Erro em generate_animation: {e}")
            return {"status": "error", "message": str(e)}
    
    # ========== FERRAMENTA 3: LIP SYNC ==========
    
    async def extract_visemes(self, audio_path: str) -> Dict:
        """
        Extrai visemas do áudio para lip sync preciso
        
        Args:
            audio_path: Caminho do arquivo de áudio
            
        Returns:
            Dict com visemas, timestamps, blend shapes
        """
        try:
            if not self.viseme_engine:
                raise ValueError("Viseme Engine não inicializado")
            
            result = await self.viseme_engine.extract(audio_path)
            self.session_data["tools_used"].append("viseme_sync")
            
            return {
                "status": "success",
                "visemes": result.get("visemes"),
                "timestamps": result.get("timestamps"),
                "blend_shapes": result.get("blend_shapes"),
                "lip_curve": result.get("lip_curve")
            }
        except Exception as e:
            logger.error(f"Erro em extract_visemes: {e}")
            return {"status": "error", "message": str(e)}
    
    # ========== FERRAMENTA 4: WEB SCRAPING ==========
    
    async def scrape_website(self, url: str, selectors: Optional[Dict] = None) -> Dict:
        """
        Faz scraping de website com BeautifulSoup/Playwright
        
        Args:
            url: URL do website
            selectors: Dicionário com seletores CSS
            
        Returns:
            Dict com dados extraídos
        """
        try:
            selectors = selectors or {}
            data = {}
            
            # Tentar com BeautifulSoup primeiro (mais rápido)
            try:
                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                for key, selector in selectors.items():
                    elements = soup.select(selector)
                    data[key] = [el.get_text(strip=True) for el in elements]
                
                self.session_data["tools_used"].append("web_scraping_bs4")
                
            except Exception as e:
                # Fallback para Playwright (para sites dinâmicos)
                logger.info(f"BeautifulSoup falhou, tentando Playwright: {e}")
                async with async_playwright() as p:
                    browser = await p.chromium.launch()
                    page = await browser.new_page()
                    await page.goto(url)
                    
                    for key, selector in selectors.items():
                        elements = await page.query_selector_all(selector)
                        data[key] = [await el.text_content() for el in elements]
                    
                    await browser.close()
                
                self.session_data["tools_used"].append("web_scraping_playwright")
            
            return {
                "status": "success",
                "url": url,
                "data": data,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Erro em scrape_website: {e}")
            return {"status": "error", "message": str(e)}
    
    # ========== FERRAMENTA 5: PROCESSAMENTO DE PDF ==========
    
    async def extract_pdf_content(self, pdf_path: str, pages: Optional[List[int]] = None) -> Dict:
        """
        Extrai conteúdo de PDF
        
        Args:
            pdf_path: Caminho do arquivo PDF
            pages: Lista de páginas para extrair (None = todas)
            
        Returns:
            Dict com texto, metadados, estrutura
        """
        try:
            content = {}
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                pages_to_extract = pages or list(range(total_pages))
                
                for page_num in pages_to_extract:
                    if page_num < total_pages:
                        page = pdf_reader.pages[page_num]
                        content[f"page_{page_num + 1}"] = page.extract_text()
            
            self.session_data["tools_used"].append("pdf_extraction")
            
            return {
                "status": "success",
                "pdf_path": pdf_path,
                "total_pages": total_pages,
                "pages_extracted": len(pages_to_extract),
                "content": content,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Erro em extract_pdf_content: {e}")
            return {"status": "error", "message": str(e)}
    
    # ========== FERRAMENTA 6: RAG TEMPORÁRIO ==========
    
    async def add_to_session_rag(self, documents: List[Dict], collection_name: str = "session_kb") -> Dict:
        """
        Adiciona documentos ao RAG temporário da sessão
        
        Args:
            documents: Lista de documentos com 'id', 'text', 'metadata'
            collection_name: Nome da coleção
            
        Returns:
            Dict com status e número de documentos adicionados
        """
        try:
            if not self.rag_client:
                raise ValueError("RAG Client não inicializado")
            
            collection = self.rag_client.get_or_create_collection(name=collection_name)
            
            ids = []
            texts = []
            metadatas = []
            
            for doc in documents:
                ids.append(doc.get("id", f"doc_{len(ids)}"))
                texts.append(doc.get("text", ""))
                metadatas.append(doc.get("metadata", {}))
            
            collection.add(ids=ids, documents=texts, metadatas=metadatas)
            
            self.session_data["tools_used"].append("rag_add")
            
            return {
                "status": "success",
                "collection": collection_name,
                "documents_added": len(documents),
                "session_id": self.session_id
            }
        except Exception as e:
            logger.error(f"Erro em add_to_session_rag: {e}")
            return {"status": "error", "message": str(e)}
    
    async def query_session_rag(self, query: str, collection_name: str = "session_kb", n_results: int = 5) -> Dict:
        """
        Consulta RAG temporário da sessão
        
        Args:
            query: Texto da consulta
            collection_name: Nome da coleção
            n_results: Número de resultados
            
        Returns:
            Dict com resultados da busca
        """
        try:
            if not self.rag_client:
                raise ValueError("RAG Client não inicializado")
            
            collection = self.rag_client.get_collection(name=collection_name)
            results = collection.query(query_texts=[query], n_results=n_results)
            
            self.session_data["tools_used"].append("rag_query")
            
            return {
                "status": "success",
                "query": query,
                "results": results,
                "session_id": self.session_id
            }
        except Exception as e:
            logger.error(f"Erro em query_session_rag: {e}")
            return {"status": "error", "message": str(e)}
    
    # ========== PIPELINE COMPLETO ==========
    
    async def full_pipeline(self, text: str, avatar_image: str, voice_profile: str = "sofia_corporate") -> Dict:
        """
        Pipeline completo: TTS → Viseme → Animação
        
        Args:
            text: Texto para Sofia falar
            avatar_image: Caminho da imagem do avatar
            voice_profile: Perfil de voz
            
        Returns:
            Dict com vídeo final, metadados, duração total
        """
        try:
            logger.info(f"Iniciando pipeline completo para Sofia...")
            
            # 1. Síntese de voz
            tts_result = await self.synthesize_speech(text, voice_profile)
            if tts_result["status"] != "success":
                return {"status": "error", "message": "Falha em TTS"}
            
            audio_path = tts_result["audio_path"]
            
            # 2. Extração de visemas
            viseme_result = await self.extract_visemes(audio_path)
            if viseme_result["status"] != "success":
                return {"status": "error", "message": "Falha em viseme extraction"}
            
            # 3. Geração de animação
            animation_result = await self.generate_animation(audio_path, avatar_image)
            if animation_result["status"] != "success":
                return {"status": "error", "message": "Falha em animação"}
            
            self.session_data["context"]["last_pipeline"] = {
                "text": text,
                "audio_path": audio_path,
                "video_path": animation_result["video_path"],
                "timestamp": datetime.now().isoformat()
            }
            
            return {
                "status": "success",
                "video_path": animation_result["video_path"],
                "audio_path": audio_path,
                "duration": tts_result.get("duration"),
                "frames": animation_result.get("frames_count"),
                "visemes_count": len(viseme_result.get("visemes", [])),
                "pipeline_duration": "~5-10 segundos por minuto de áudio"
            }
        except Exception as e:
            logger.error(f"Erro em full_pipeline: {e}")
            return {"status": "error", "message": str(e)}
    
    # ========== UTILITÁRIOS ==========
    
    def get_session_info(self) -> Dict:
        """Retorna informações da sessão atual"""
        return {
            "session_id": self.session_id,
            "created_at": self.session_data["created_at"],
            "tools_used": list(set(self.session_data["tools_used"])),
            "context": self.session_data["context"]
        }
    
    def export_session(self) -> str:
        """Exporta dados da sessão como JSON"""
        return json.dumps(self.session_data, indent=2, default=str)


if __name__ == "__main__":
    # Teste
    async def test_sofia():
        sofia = SofiaEngine()
        await sofia.initialize_engines()
        
        # Teste de síntese de voz
        result = await sofia.synthesize_speech(
            "Olá, eu sou Sofia, sua assistente digital completa.",
            "sofia_corporate"
        )
        print(f"TTS Result: {result}")
        
        # Informações da sessão
        print(f"\nSession Info: {sofia.get_session_info()}")
    
    # asyncio.run(test_sofia())
