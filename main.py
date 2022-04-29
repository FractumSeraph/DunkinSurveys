from splinter import Browser


def submitsurvey(number, comment):
    browser = Browser()  # defaults to firefox
    browser.visit('http://dunkinrunsonyou.com/')
    browser.fill('spl_q_inrest_rcpt_code_txt', number)
    browser.find_by_name('forward_main-pager').click()

    if browser.is_text_present("How likely are you to recommend Dunkin' to a friend or family member"):
        print("Survey code entered.")
    else:
        print("Something is incorrect. 1")

    browser.find_by_id("onf_q_inrest_recommend_ltr_11").click()
    browser.find_by_id("onf_q_inrest_recent_experience_osat_5").click()
    browser.fill('spl_q_inrest_score_cmt', comment)
    browser.find_by_id("buttonNext").click()

    if browser.is_text_present("Based on your visit, how satisfied were you with the following areas"):
        print("First page completed, loaded page two.")
    else:
        print("Something is incorrect. 2")

    browser.find_by_id("onf_q_inrest_speed_of_service_osat_5").click()
    browser.find_by_id("onf_q_inrest_appearence_of_the_restraunt_osat_5").click()
    browser.find_by_id("onf_q_inrest_taste_of_food_osat_5").click()
    browser.find_by_id("onf_q_inrest_friendliness_of_staff_osat_5").click()
    browser.find_by_id("onf_q_inrest_order_fulffiled_yn_1").click()
    browser.find_by_id("onf_q_inrest_visit_experience_yn_2").click()
    browser.find_by_id("buttonNext").click()

    if browser.is_text_present(
            "We appreciate your feedback. As a thank you, we would like to email you a coupon for a"):
        print("Second page completed, loaded page three.")
    else:
        print("Something is incorrect. 3")

    browser.find_by_id("onf_q_inrest_rcpt_additional_questions_alt_2").click()
    browser.find_by_id("buttonNext").click()
    print("Survey complete")


print("Enter the survey code. (Numbers only)")
surveyCode = str(input())
if len(surveyCode) != 18:
    print("Error. Survey code should be 18 numbers.")
    quit(2)

print("Enter the nice comment you want to make.")
surveyComment = str(input())

submitsurvey(surveyCode, surveyComment)

print("Script has finished.")
