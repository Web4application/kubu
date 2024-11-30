// Make sure to include these imports:
// import { GoogleGenerativeAI } from "@google/generative-ai";
const genAI = new GoogleGenerativeAI(process.env.AIzaSyAvrxOyAVzPVcnzxuD0mjKVDyS2bNWfC10);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

const prompt = "### Fantasy
1. "Describe a world where the seasons are controlled by mythical creatures."
2. "A young wizard discovers an ancient spellbook that can alter reality."
3. "A dragon and a knight form an unlikely alliance to save their kingdom."

### Science Fiction
1. "Write about a future where humans can upload their consciousness into a digital world."
2. "In a world where time travel is possible, a historian accidentally changes a major event in history."
3. "In a future where humans live on Mars, a scientist discovers a hidden alien civilization."

### Mystery
1. "A detective receives an anonymous tip that leads them to a hidden room in an old mansion."
2. "A journalist uncovers a series of coded messages hidden in famous paintings."
3. "A librarian finds a secret compartment in an old book that leads to a decades-old mystery."

### Romance
1. "Two people meet in a bookstore and discover they have a shared love for an obscure author."
2. "Two people from rival families fall in love and must navigate their secret relationship."
3. "Two people meet through a series of anonymous love letters left in a public park."

### Adventure
1. "A group of friends find a treasure map in an old attic and decide to follow it."
2. "An explorer finds a hidden civilization in the depths of the Amazon rainforest."
3. "A young archaeologist discovers a map leading to a lost city beneath the ocean."

### Horror
1. "A family moves into a new house, only to find out itâs haunted by its previous inhabitants."
2. "A group of friends play a seemingly innocent game that turns deadly."
3. "A group of friends accidentally summon a vengeful spirit during a camping trip."

### Historical Fiction
1. "Write a story set during the Renaissance, focusing on an artist who discovers a secret about their most famous painting."
2. "A soldier during World War II discovers a hidden talent that changes the course of their life."
3. "A young woman in Victorian England disguises herself as a man to become a detective."

### Magical Realism
1. "In a small town, everyone has a unique magical ability that manifests on their 18th birthday."
2. "In a city where everyone has a guardian spirit, one person is born without one."
3. "In a town where everyone has a unique magical power, one personâs power is to bring paintings to life."

### Dystopian
1. "In a world where emotions are regulated by the government, one person starts to feel something different."
2. "In a society where books are banned, a secret group of rebels fights to preserve literature."
3. "In a world where emotions are illegal, a rebel group fights to restore human feelings."

### Slice of Life
1. "A day in the life of a street performer in a bustling city."
2. "A day in the life of a barista who dreams of becoming a famous musician."
3. "A day in the life of a street artist who paints murals that tell the stories of the city's residents."
.";

const result = await model.generateContent(prompt);
console.log(result.response.text());
