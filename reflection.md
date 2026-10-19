# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
(Answer): So I am using the following classes: Pet, Scheduler, owner, and scheduler. They are recomended classes from the assignment and I felt they functioned well. Under pet I ensured that the aattributes had to do with identifiers for the pet such as name and species. Under task I included task descriptions , completions , timing, etc.. Owner functions to keep track of multiple pets, Owner holds a list of Pet objects, so each pet stays separate. Say that directly.  Scheduler functions as the class where it all comes together and a Plan is produced

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
(ANSWER): One change I made based on the AI's suggestion had to do with task timings. So in the original diagram, there was no way to distinguish between hard deadlines and recomended timings, this of course means the diagram would treat a scheduled walk time and qa scheduled medication time as the same. I felt there ought to be a distinction espescially since a walk can vary in how long it takes.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Trade

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

(Answer): For the algorithm task.mark_complete(), the AI suggested it suggested I remove the completion_date varibale. Much of this variables function is already done by completed_occurence. However completion_date variable can help prevent issues if future logic regarding chronological order is added. It makes it eas Considering some pets can have health issues it may be improtant to use such logic.

---

## 3. AI Collaboration
(ANSWER): The genral structure of the classes, the attributes, and methods were provided by me. As we went along those struvutres became subject to more and more change, this is where the AI shined. I accepted most of its recomendations with the exception of its suggestions with the attributes. Copilot recomended a simplification of the attributs, a more genralized set of tasks. However I felt the complexity was needed considering this app was meant for the care of living creatures. 
**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

(ANSWER): It waa very helpful in clearing up confusing code logic or errors. I felt it helped significantly in keeping track of the tangled web of features, methods, classes and their interactions.  

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---
(AMSWER): There was one point where the AI had asked me to cut down on the features. However I felt it would leave the app unable to account for edge cases such as a sick animal or one with very specific dietary restrictions. There was certainly a pull from the AI to standardize things and I think that pull ignores those edge cases 

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

(ANSWER) I ensured to test for the Apps ability to remeber. It was the core of the whole project and I feel the app does a good job of parsing between pets, their tasks, and so on

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---
(Answer): I actually noticed an issue with the owners part of the project. I wish I could have tested more in the codebase to find where the issue originated. it does not do a good job remebering owners
## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
(Answer): I would say I am satisfied with how I have learned to use the AI. 
**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
(ANSWER): I am not happy with my oversight on the owners issue. I need to better track the changes being made
**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
(ANSWER): AI is only as good as the person keeping an eye on it. 