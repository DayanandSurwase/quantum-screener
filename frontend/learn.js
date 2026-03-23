let currentDeck = [];
let currentIndex = 0;

const generateCardsBtn = document.getElementById("generateCardsBtn");
const topicInput = document.getElementById("topicInput");
const loader = document.getElementById("loader");
const deckArea = document.getElementById("deckArea");
const flashcardWrapper = document.getElementById("flashcardWrapper");
const flashcard = document.getElementById("flashcard");

generateCardsBtn.addEventListener("click", async () => {
  const topic = topicInput.value.trim();
  if (!topic) return;

  // UI Reset
  generateCardsBtn.disabled = true;
  generateCardsBtn.innerText = "GENERATING...";
  deckArea.classList.add("hidden");
  loader.classList.remove("hidden");

  try {
    console.log(`Sending request for topic: ${topic}`); // Debug log

    const response = await fetch("/api/learn", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic: topic }),
    });

    const data = await response.json();
    console.log("AI Response Data:", data);

    if (!response.ok) throw new Error(data.detail || "API Error");

    // Ensure data is an array before trying to map it
    if (Array.isArray(data.flashcards) && data.flashcards.length > 0) {
      currentDeck = data.flashcards;
    } else {
      // Fallback if AI messed up the JSON
      currentDeck = [
        {
          question: "Format Error",
          answer:
            "The AI generated the text, but not in strict JSON. Try generating again.",
        },
      ];
    }

    currentIndex = 0;
    flashcard.classList.remove("flipped");
    updateCard();

    // Show the cards
    loader.classList.add("hidden");
    deckArea.classList.remove("hidden");
  } catch (error) {
    console.error("Fetch error:", error);
    loader.classList.add("hidden");
    alert("Failed to generate deck: " + error.message);
  } finally {
    generateCardsBtn.disabled = false;
    generateCardsBtn.innerText = "GENERATE";
  }
});

topicInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        generateCardsBtn.click();
    }
});

// 3D Flip logic explicitly toggles the class
flashcardWrapper.addEventListener("click", () => {
  console.log("Card clicked! Toggling flip...");
  flashcard.classList.toggle("flipped");
});

// Navigation logic
document.getElementById("prevBtn").addEventListener("click", () => {
  if (currentIndex > 0) {
    flashcard.classList.remove("flipped");
    setTimeout(() => {
      currentIndex--;
      updateCard();
    }, 300);
  }
});

document.getElementById("nextBtn").addEventListener("click", () => {
  if (currentIndex < currentDeck.length - 1) {
    flashcard.classList.remove("flipped");
    setTimeout(() => {
      currentIndex++;
      updateCard();
    }, 300);
  }
});

function updateCard() {
  if (currentDeck.length === 0) return;
  document.getElementById("cardFront").innerText =
    currentDeck[currentIndex].question || "Unknown Question";
  document.getElementById("cardBack").innerText =
    currentDeck[currentIndex].answer || "Unknown Answer";
  document.getElementById("cardCounter").innerText =
    `${currentIndex + 1} / ${currentDeck.length}`;
}
