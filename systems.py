class Systems:
    _brain = None
    _audio = None
    
    @classmethod
    def get_brain(cls):
        if cls._brain is None:
            print("Initializing Brain (Singleton)...")
            from brain import ShipraBrain  # Lazy Import
            cls._brain = ShipraBrain()
        return cls._brain
        
    @classmethod
    def get_audio(cls):
        if cls._audio is None:
            print("Initializing Audio System (Singleton)...")
            from audio import ShipraAudio  # Lazy Import
            cls._audio = ShipraAudio()
        return cls._audio
