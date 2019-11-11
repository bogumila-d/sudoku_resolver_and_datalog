#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 14:38:21 2017

@author: tugg
update: vissejul, bachmdo2, stdm (Nov 27, 2018)
"""
import pandas as pa
from pyDatalog import pyDatalog

# ---------------------------------------------------------------------------
# Social graph analysis:
# work through this code from top to bottom (in the way you would use a R or Jupyter notebook as well...) and write datalog clauses
# and python code in order to solve the respective tasks. Overall, there are 7 tasks.
# ---------------------------------------------------------------------------

@pyDatalog.program()
def _():

    calls = pa.read_csv('calls.csv', sep='\t', encoding='utf-8')
    texts = pa.read_csv('texts.csv', sep='\t', encoding='utf-8')
    suspect = 'Quandt Katarina'
    company_Board = ['Soltau Kristine', 'Eder Eva', 'Michael Jill']
    pyDatalog.create_terms('knows, '
                           'has_link, '
                           'all_connections, '
                           'max_five_people, '
                           'helper')

    # First, treat calls as simple social links (denoted as knows), that have no date
    # the caller knows callee
    for i in range(len(calls)):
        +knows(calls.iloc[i, 1], calls.iloc[i, 2])
        # Task 1: Knowing someone is a bi-directional relationship -> define the predicate accordingly
    knows(X, Y) <= knows(Y, X) & (X != Y)

    print(knows(suspect, Y))

    # Task 2: Define the predicate has_link in a way that it is true if a connection exists
    # (path of people knowing the next link)
    # Hints:
    # check if your predicate works: at least 1 of the following asserts should be true
    # (2 if you read in all 150 communication records)
    #   (be aware of the unusual behaviour that if an assert evaluates as true, an exception is thrown)

    has_link(X, Y) <= knows(X, Z) & has_link(Z, Y) & (X != Y)
    has_link(X, Y) <= knows(X, Y)

    assert (has_link('Quandt Katarina', company_Board[0]) == ())
    # assert (has_link('Quandt Katarina', company_Board[1]) == ())
    # assert (has_link('Quandt Katarina', company_Board[2]) == ())

    # 'Quandt Katarina' knows 'Eder Eva' and 'Michael Jill'

    # Task 3: You already know that a connection exists; now find the concrete paths between the board members
    # and the suspect
    # Hints:
    #   if a knows b, there is a path between a and b
    #   (X._not_in(P2)) is used to check whether x is not in path P2
    #   (P==P2+[Z]) declares P as a new path containing P2 and Z

#     path(Y,Y,P) <=  (P==[Y])
# path(X,Y,P) <= path(X,Z,P2) & knows(Z,Y) & (Y._not_in(P2)) &  (X!=Y)  & (P==P2 + [Y])

    helper(X, Y, P2) <= (X != Y) & (X._not_in(P2)) & (Y._not_in(P2))

    all_connections(X, Y, P) <= all_connections(X, Z, P2) & knows(Z, Y) & helper(X, Y, P2) & (P == P2+[Z])
    all_connections(X, Y, P) <= knows(X, Y) & (P == [])

    # Task 4: There are too many paths. We are only interested in short paths.
    # Find all the paths between the suspect and the company board that contain five people or less

    # (max_five_people(X, Y, P, C)) <= (max_five_people(X, Z, P2, C2)) & all_connections(X, Y, P) & (C == C2 + 1) & (C <= 2)

    (max_five_people(X, Y, P, C)) <= (max_five_people(X, Z, P2, C2)) & knows(Z, Y) \
    & helper(X, Y, P2) & (P == P2+[Z]) & (C == C2 + 1) & (C <= 2)
    (max_five_people(X, Y, P, C)) <= knows(X, Y) & (P == []) & (C == 0)

    for member in company_Board:
        print("Who ", suspect, "/", member)
        print(max_five_people(suspect, member, P, C))
        print("Who ", member, "/", suspect)
        print(max_five_people(member, suspect, P, C))

    # ---------------------------------------------------------------------------
    # Call-Data analysis:
    # Now we use the text and the calls data together with their corresponding dates
    # ---------------------------------------------------------------------------
    date_board_decision = '12.2.2017'
    date_shares_bought = '23.2.2017'

    pyDatalog.create_terms('called, texted, descending_communication, data_valid')
    pyDatalog.clear()
    for i in range(len(calls)):  # calls
        +called(calls.iloc[i, 1], calls.iloc[i, 2], calls.iloc[i, 3])
    for i in range(len(texts)):  # texts
        +texted(texts.iloc[i, 1], texts.iloc[i, 2], texts.iloc[i, 3])

    # calls are bi-directional
    called(X, Y, Z) <= called(Y, X, Z)

    # Task 5: Again we are interested in links, but this time a connection is only valid
    # if the links are descending in date;
    #         find out who could have actually sent the information by adding this new restriction
    # Hints:
    #   You are allowed to naively compare the dates lexicographically using ">" and "<";
    #   it works in this example (but is evil in general)

    data_valid(D) <= (D >= date_board_decision) & (D <= date_shares_bought)
    helper(X, Y, P, P2, D, D2) <= (X != Y) & (X._not_in(P2)) & (Y._not_in(P2)) & (P == P2+[D2]+[Y]+[D])

    print("descending_communication")
    (descending_communication(X, Y, D, P)) <= \
    (descending_communication(X, Z, D2, P2)) & (called(Z, Y, D) or texted(Z, Y, D)) & helper(X, Y, P, P2, D, D2)\
    & data_valid(D) & data_valid(D2) & (D < D2)
    (descending_communication(X, Y, D, P)) <= called(X, Y, D) & (P == [Y])

    # (descending_communication(X, Y, D, P)) <= \
    # (descending_communication(X, Z, D2, P2)) & texted(Z, Y, D) & (X != Y) & \
    # (X._not_in(P2)) & (Y._not_in(P2)) & (P == P2+[D2]+[Y]+[D]) & \
    # (D >= date_board_decision) & (D <= date_shares_bought) & (D < D2) & (D2 >= date_board_decision) & (D2 <= date_shares_bought)
    # (descending_communication(X, Y, D, P)) <= texted(X, Y, D) & (P == [Y])

    # D2 ist das Datum des vorhergehenden Anrufs / Kommunikation

    # Task 6: Find all the communication paths that lead to the suspect
    # (with the restriction that the dates have to be ordered correctly)

    for member in company_Board:
        print("From ", suspect, 'to ', member)
        print(descending_communication(suspect, member, D, P))
        print("From ", member, "to ", suspect)
        print(descending_communication(member, suspect, D, P))

    # Final task: after seeing this information, who, if anybody, do you think gave a tip to the suspect?

    # EDER EVA

    # General hint (only use on last resort!):
    # if nothing else helped, have a look at
    # https://github.com/pcarbonn/pyDatalog/blob/master/pyDatalog/examples/graph.py
