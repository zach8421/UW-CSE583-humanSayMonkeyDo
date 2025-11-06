## Who is the user
Alice is a cognitive neuroscience researcher who studies language, motor control, and brain function. She is familiar with research papers, experimental designs, and theoretical models in neuroscience. However, she does not have a strong background in programming, neural signal preprocessing, or machine learning pipelines. She often collaborates with technical lab members but prefers tools that minimize code complexity and data-wrangling overhead.

## What do they want to do with the tool
Alice wants to use this tool to compare neural activity patterns between humans performing (or attempting) speech and monkeys performing reaching movements. She aims to explore whether mouth/tongue kinematics during speech attempt can be represented and analyzed similarly to arm movement kinematics. She wants to be able to quickly upload datasets, visualize neural responses across trials, and identify whether similar population-level patterns exist across species.

## What needs and desires do they want for the tool
Alice desires a tool that abstracts away complex preprocessing and formatting steps. Specifically, she needs:

- A **simple interface** to load the monkey dataset (already structured) and the human dataset (which needs preprocessing).
- **Automated preprocessing** steps that convert human phonemes into pseudo-kinematic features and align trials without requiring manual code editing.
- **Side-by-side visualizations** of neural activity during reaching vs. attempted speech.
- **Built-in analysis modules** for:
  - Movement onset detection  
  - Single-neuron tuning curve visualization  
  - Target/phoneme position decoding using linear/logistic models  
- **Clear explanations** of results, ideally in natural language (“This neuron shows directional tuning similar to motor cortex tuning during reaching tasks”).
- The ability to **export plots, summaries, and analysis reports** for lab meetings or manuscripts.

## What is their skill level
Alice is highly knowledgeable in neuroscience theory and research interpretation. She excels at understanding neural function conceptually and critically evaluating results. However, she has **limited programming experience** and prefers point-and-click or guided workflows over command-line scripts. The tool should therefore:

- Provide **no-code or low-code interactions**
- Offer **guided step-by-step interface flows**
- Use **intuitive plots and vocabulary**, avoiding heavy mathematical jargon unless requested

