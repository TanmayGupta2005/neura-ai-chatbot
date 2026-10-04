import express from "express";
import cors from "cors";
import axios from "axios";

const app = express();

app.use(cors());
app.use(express.json());

const PORT = 5000;
const ML_SERVICE_URL = "http://127.0.0.1:8001";


app.get("/", (req, res) => {
    res.json({
        message: "AI Chatbot Backend is running"
    });
});


app.post("/api/chat", async (req, res) => {

    try {

        const { message, conversation = [] } = req.body;

        if (!message) {
            return res.status(400).json({
                error: "Message is required"
            });
        }


        const response = await axios.post(
            `${ML_SERVICE_URL}/predict`,
            {
                message,
                conversation
            }
        );


        res.json({
            message,
            reply: response.data.reply,
            intent: response.data.intent,
            confidence: response.data.confidence
        });


    } catch (error) {

        console.error(
            "ML Service Error:",
            error.message
        );


        res.status(500).json({
            error: "Could not connect to ML service"
        });

    }

});


app.listen(PORT, () => {

    console.log(
        `Backend running on http://localhost:${PORT}`
    );

});