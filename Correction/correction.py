from correction_lib import Create_Confusion_Matrix, All_Ground_Truth_Words, Compute_Pr_c
from correction_lib import getLetterIndex, CreateChars, Find_Possible_Candidates
from correction_lib import Ground_Truth_Words
from Create_Words_Dictionary import Create_Words_Dictionary

Ground_Truth_Words_Dictionary = Create_Words_Dictionary()

# correct_word = "oberstar"
#
# neighbor = "the"
#
# r = 0
#
# if neighbor in Ground_Truth_Words_Dictionary[correct_word]["left"]:
#     r = Ground_Truth_Words_Dictionary[correct_word]["left"][neighbor]
#
# Nr = 0
#
# for lword in Ground_Truth_Words_Dictionary[correct_word]["left"]:
#     if Ground_Truth_Words_Dictionary[correct_word]["left"][lword] == r:
#         Nr += 1
#
# if Nr == 0:
#     Nr = len(Ground_Truth_Words_Dictionary) - len(Ground_Truth_Words_Dictionary[correct_word]["left"])
#
# print(r)
#
# Nr1 = 0
#
# for lword in Ground_Truth_Words_Dictionary[correct_word]["left"]:
#     if Ground_Truth_Words_Dictionary[correct_word]["left"][lword] == r+1:
#         Nr1 += 1
#
# r_star = (r+1)*Nr1/Nr
#
# print(r_star)
#
# N_Star = 0
#
# for r_index in range(r):
#     Temp_Nr = 0
#     for lword in Ground_Truth_Words_Dictionary[correct_word]["left"]:
#         if Ground_Truth_Words_Dictionary[correct_word]["left"][lword] == r_index:
#             Temp_Nr += 1
#     print(Temp_Nr)
#     N_Star = N_Star + r_star*Temp_Nr

# print(r)
# print(Nr)
# print(N_Star)
Confusion = Create_Confusion_Matrix()

Deletion_Confusion = Confusion["Deletion_Confusion"]

Insertion_Confusion = Confusion["Insertion_Confusion"]

Substitution_Confusion = Confusion["Substitution_Confusion"]

Reversal_Confusion = Confusion["Reversal_Confusion"]

charsX = CreateChars()["charsX"]

charsXY = CreateChars()["charsXY"]

typo = "representatlves"

Possible_Candidates = Find_Possible_Candidates(typo)

# This function will compute its p(t|c) for each candidates input

def Find_Candidates_P_T_C_P_C(Candidates):
    Candidates_Possibility = list()
    Typo = Candidates["Typo"]
    Candidates = Candidates["Possible_Candidates"]

    for Candidate in Candidates:
        Candidate_List = Candidates[Candidate]
        if len(Candidate_List) >= 1:

            if Candidate == "Insertion":
                for candidate in Candidate_List:
                    correct, letter, position = candidate
                    # c_p_minus_1 = ""
                    if position - 1 < 0:
                        c_p_minus_1 = " "
                    else:
                        c_p_minus_1 = correct[position-1]
                    t_p = letter
                    add_cpMinus1_tp = Insertion_Confusion[getLetterIndex(c_p_minus_1)][getLetterIndex(t_p)]
                    chars_cpMinus1 = charsX[getLetterIndex(c_p_minus_1)]
                    Candidates_Possibility.append({"Typo": Typo, "Cor": correct, "p_t_c" : add_cpMinus1_tp/chars_cpMinus1, "p_c" : Compute_Pr_c(correct), "p_t_c_p_c" : Compute_Pr_c(correct)*add_cpMinus1_tp/chars_cpMinus1})

            elif Candidate == "Deletion":
                for candidate in Candidate_List:
                    correct, position = candidate
                    # c_p_minus_1 = ""
                    if position - 1 < 0:
                        c_p_minus_1 = " "
                    else:
                        c_p_minus_1 = correct[position-1]
                    c_p = correct[position]
                    del_cpMinus1_cp = Deletion_Confusion[getLetterIndex(c_p_minus_1)][getLetterIndex(c_p)]
                    chars_cpMinus1_cp = charsXY[getLetterIndex(c_p_minus_1)][getLetterIndex(c_p)]
                    Candidates_Possibility.append({"Typo": Typo, "Cor": correct, "p_t_c" : del_cpMinus1_cp/chars_cpMinus1_cp, "p_c" : Compute_Pr_c(correct), "p_t_c_p_c" : Compute_Pr_c(correct)*add_cpMinus1_tp/chars_cpMinus1})

            elif Candidate == "Reverse":
                for candidate in Candidate_List:
                    correct, pre, pos = candidate
                    c_pre = correct[pre]
                    c_pos = correct[pos]
                    rev_c_pre_c_pos = Reversal_Confusion[getLetterIndex(c_pre)][getLetterIndex(c_pos)]
                    chars_c_pre_c_pos = charsXY[getLetterIndex(c_pre)][getLetterIndex(c_pos)]
                    Candidates_Possibility.append({"Typo": Typo, "Cor": correct, "p_t_c" : rev_c_pre_c_pos/chars_c_pre_c_pos, "p_c" : Compute_Pr_c(correct), "p_t_c_p_c" : Compute_Pr_c(correct)*add_cpMinus1_tp/chars_cpMinus1})

            elif Candidate == "Substitution":
                for candidate in Candidate_List:
                    correct, letter, position = candidate
                    # c_p_minus_1 = ""
                    c_p = correct[position]
                    t_p = letter
                    sub_tp_cp = Insertion_Confusion[getLetterIndex(t_p)][getLetterIndex(c_p)]
                    chars_cp = charsX[getLetterIndex(c_p)]
                    Candidates_Possibility.append({"Typo": Typo, "Cor": correct, "p_t_c" : sub_tp_cp/chars_cp, "p_c" : Compute_Pr_c(correct), "p_t_c_p_c" : Compute_Pr_c(correct)*add_cpMinus1_tp/chars_cpMinus1})

    return(Candidates_Possibility)



# print(Find_Candidates_P_T_C_P_C(Possible_Candidates))
