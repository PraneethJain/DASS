#align(center, text(17pt)[*Design and Analysis of Software Systems*])
#align(center, text(16pt)[Class Activity - Submarine Pod])
#align(center, text(13pt)[Moida Praneeth Jain, 2022101093])
#align(center, text(13pt)[Divyansh Jain, 2022101125])

= Prompts Used:
- ```
- Design a system to facilitate entry and exit into underwater submarine pods
- Entry/Exit chamber (2 latches for air and water pressure)
- At any point of time, atleast one of the latches should be closed
- Control Panel to control both the outer and inner latches
- Open the outer latch only when chamber is filled with water
- Open the inner latch only when chamber is drained

Output as plantuml
```
- ```
the sequence of events is as follows:
water is filled
outer latch is opened
outer latch is closed
water is drained
inner latch is opened
inner latch is closed
```
- Add a pause and resume feature for draining and filling
- Give UML Class Diagram
- Give UML State Diagram
- Give UML Sequence Diagram

= Tool Used:
- PlantUML

= Class Diagram

#figure(image("class_diagram.png", height: 35%))

= State Diagram

#figure(image("state_diagram.png", height: 95%))

= Sequence Diagram
#figure(image("sequence_diagram.png", width: 100%))