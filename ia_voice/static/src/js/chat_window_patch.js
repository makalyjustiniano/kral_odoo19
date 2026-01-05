import { Composer } from "@mail/core/common/composer";
import { patch } from "@web/core/utils/patch";

console.log("Cargando parche IA Voice en Composer");

patch(Composer.prototype, {
    setup() {
        super.setup(...arguments);
        this.recognition = null;
        this.transcript = "";
        this.initSpeechRecognition();
    },

    initSpeechRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = true;
            this.recognition.interimResults = true;
            this.recognition.lang = 'es-ES';  

            this.recognition.onresult = (event) => {
                let finalTranscript = '';
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    if (event.results[i].isFinal) {
                        finalTranscript += event.results[i][0].transcript;
                    }
                }
                if (finalTranscript) {
                    this.transcript += finalTranscript;
                    console.log("Transcript final:", this.transcript);
                }
            };

            this.recognition.onerror = (event) => {
                console.error("Error en reconocimiento de voz:", event.error);
                if (event.error === 'network') {
                    console.log("Reintentando reconocimiento debido a error de red...");
                    setTimeout(() => {
                        if (this.recognition) {
                            this.recognition.start();
                        }
                    }, 1000);  
                }
            };

            this.recognition.onend = () => {
                console.log("Reconocimiento terminado");
                if (this.transcript) {
                    this.insertTranscriptIntoComposer();
                }
            };
        } else {
            console.warn("Speech Recognition no soportado en este navegador");
        }
    },

    onStartVoiceRecognition() {
        if (this.recognition) {
            this.transcript = "";
            this.recognition.start();
            console.log("Reconocimiento de voz iniciado");
        }
    },

    onStopVoiceRecognition() {
        if (this.recognition) {
            this.recognition.stop();
            console.log("Reconocimiento de voz detenido");
        }
    },

    insertTranscriptIntoComposer() {
        console.log("Insertando transcript en el composer:", this.transcript);
        if (this.props.composer) {
            this.props.composer.insertText(this.transcript);
            
        }
    }
});