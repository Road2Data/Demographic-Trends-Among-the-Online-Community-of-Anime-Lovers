import numpy as np
import pandas as pd

ageScale = {
    "17 or under": 0,
    "18 - 25": 1,
    "26 - 33": 2,
    "34 - 41": 3,
    "42 - 49": 4,
    "50 - 57": 5,
    "58 - 65": 6,
    "65 +": 7,
    np.nan: np.nan
}

def binGender(seriesCell):
    if seriesCell == "Man":
        return "Man"
    elif seriesCell == "Woman":
        return "Woman"
    elif seriesCell in ['GNC or Genderqueer', 'Fluid or Multigender', 'Agender', 'Otherwise Nonbinary']:
        return "Enby"
    else:
        return np.nan

bitExtractor = {
    "Yes": 1,
    "No": 0,

    "Subs": 1,
    "Dubs": 0,
    np.nan: np.nan
}

abbreviationsOne = {
    # For use in "Clean Data.csv" file
    "Some high school": "HSDropout",
    "High School Diploma / GED": "HS",
    "Trade / Vocational School": "T/VS",
    "Associate's": "AA/AS",
    "Bachelor's": "BA/BS",
    "Master's": "MS",
    "Ph.D.": "PhD",

    "Unemployed": "Unemployed",
    "Part-time worker": "PartTimer",
    "Full-time": "FullTimer",

    "On live TV": "platformTV",
    "A generalized streaming service such as Netlfix, Hulu, or Amazon Prime Video": "GSS",
    # Typo in original survey
    "An anime-focused streaming service such as VRV, Crunchyroll, or Funimation": "AFSS",
    "Personal copies, such as DVDs, Blu-Rays, or season purchases": "COPY",
    "Other sources": "OTHER",
    "I don't watch anime.": "N/A",

    "Action": "Action",
    "Comedy, including Slice-of-Life": "Comedy/SoL",
    "Fantasy / Issekai": "Fantasy",
    "Romance / Drama": "Rom/Dram",
    "Sci-Fi, including Military and Mecha": "SciFi/M&M",
    "Supernatural / Magic": "Supernatural",
    "Tragedy / Psychological": "Psycho",

    np.nan: np.nan
}

abbreviationsTwo = {
    # For use in the "Machine-Readable Data.csv" file
    # For nominal variables that will require bitwise (dummy) encoding
    "North America": "locNA",
    "South America": "locSA",
    "Europe": "locEu",
    "Asia": "locAs",
    "Australia": "locOc",
    # Respondents in the Oceania region responded Australia

    "Some high school": "eduHSDropout",
    "High School Diploma / GED": "eduHS",
    "Trade / Vocational School": "eduT/VS",
    "Associate's": "eduAA/AS",
    "Bachelor's": "eduBA/BS",
    "Master's": "eduMS",
    "Ph.D.": "eduPhD",

    "Unemployed": "isUnemployed",
    "Part-time worker": "isPartTimer",
    "Full-time": "isFullTimer",

    "On live TV": "platformTV",
    "A generalized streaming service such as Netlfix, Hulu, or Amazon Prime Video": "platformGSS",
    # Typo in original survey
    "An anime-focused streaming service such as VRV, Crunchyroll, or Funimation": "platformAFSS",
    "Personal copies, such as DVDs, Blu-Rays, or season purchases": "platformCOPY",
    "Other sources": "platformOTHER",
    "I don't watch anime.": "platformN/A",

    np.nan: np.nan
}

def getGMT(seriesCell):
    """Classify timezones and return a floating-point to represent GMT offset."""
    e = str(seriesCell).strip().upper()

    if e in ["COTE", "WET", "UTC", "GMT"]:
        t = 0.0
    elif e in ["CET", "BST", "MEZ", "UTC+1", "GMT+1"]:
        t = 1.0
    elif e in ["CEST", "EET", "MT", "UTC+2", "GMT+2"]:
        t = 2.0
    elif e in ["EEST", "UTC+3", "GMT+3"]:
        t = 3.0
    elif e in ["GST", "UTC+4"]:
        t = 4.0
    elif e == "UTC+5":
        t = 5.0
    elif e in ["IST", "UTC+5:30", "GMT+5:30"]:
        t = 5.5
    elif e == "NPT":
        t = 5.75
    elif e == "GMT+6:30":
        t = 6.5
    elif e in ["ICT", "THA", "WIB", "UTC+7"]:
        t = 7.0
    elif e in ["HKT", "SGT", "MYT", "GMT+8"]:
        t = 8.0
    elif e == "GMT+8:30":
        t = 8.5
    elif e == "JST":
        t = 9.0
    elif e == "ACST":
        t = 9.5
    elif e in ["AEST", "GMT+10"]:
        t = 10.0
    elif e == "ACDT":
        t = 10.5
    elif e == "AEDT":
        t = 11.0
    elif e in ["NZDT", "NZT", "GMT+13"]:
        t = 13.0
    elif e in ["BRT", "ADT", "UTC-3", "GMT-3"]:
        t = -3.0
    elif e == "CNT":
        t = -3.5
    elif e in ["AST", "EDT", "GMT-4"]:
        t = -4.0
    elif e in ["EST", "ET", "ETC", "UTC-5", "GMT-5"]:
        t = -5.0
    elif e in ["CST", "CTL", "USCT", "UTC-6", "GMT-6"]:
        t = -6.0
    elif e in ["MDT", "MST", "MT", "PDT"]:
        t = -7.0
    elif e in ["LAX", "PCT", "PST", "PT", "PSR", "PAC", "GMT-8"]:
        t = -8.0
    elif e == "AKST":
        t = -9.0
    elif e == "HST":
        t = -10.0
    else:
        # Fail condition
        t = np.nan
    return t

def getConsumptionSources(series):
    # Transform a "Check all that apply" into an array of bits.
    # Essentially, pd.get_dummies(series.apply(lambda x: x.split(";"))), but cleaner.
    bits = np.zeros((483, 5))
    i = 0
    for cell in series:
        if cell == np.nan:
            bits[i] = [np.nan, np.nan, np.nan, np.nan, np.nan]
        else:
            if "Anime" in str(cell):
                bits[i][0] = 1
            if "Manga" in str(cell):
                bits[i][1] = 1
            if "Doujinshi" in str(cell):
                bits[i][2] = 1
            if "Light Novels" in str(cell):
                bits[i][3] = 1
            if "Visual Novels" in str(cell):
                bits[i][4] = 1
        i+= 1

    sources = pd.DataFrame(data=np.array(bits), columns=['watchesAnime', "readsManga", "readsDoujins", "readsLNs", "playsVNs"])
    return sources

genre_one = {
    "Action": "1favAction",
    "Comedy, including Slice-of-Life": "1favComedy/SoL",
    "Fantasy / Issekai": "1favFantasy",
    "Romance / Drama": "1favRom/Dram",
    "Sci-Fi, including Military and Mecha": "1favSciFi/M&M",
    "Supernatural / Magic": "1favSupernatural",
    "Tragedy / Psychological": "1favPsycho"
}

genre_two = {
    "Action": "2favAction",
    "Comedy, including Slice-of-Life": "2favComedy/SoL",
    "Fantasy / Issekai": "2favFantasy",
    "Romance / Drama": "2favRom/Dram",
    "Sci-Fi, including Military and Mecha": "2favSciFi/M&M",
    "Supernatural / Magic": "2favSupernatural",
    "Tragedy / Psychological": "2favPsycho"
}

overH_ans = {"Yes": "overHYes", "No": "overHNo", "Maybe": "overHMaybe", np.nan: np.nan}
inclusivity = {"Yes": "socIncYes", "No": "socIncNo", "Maybe": "socIncMaybe", np.nan: np.nan}

if __name__ == '__main__':
    rr = pd.read_csv("SurveyResponses.csv")
    # raw responses

    # Clean Data.csv will...
    #   * Rename columns and entries for easy queries
    #   * Apply some binning, in the case of gender
    #   * Extract gmtOffset
    #   * Represent yes/no responses as bits
    cd = pd.DataFrame()
    cd["ageRange"] = rr["How old are you?"].apply(lambda x: ageScale[x])
    cd["gender"] = rr["Which of the following best describes your gender identity?"].apply(lambda x: binGender(x))
    cd["isLGBT+"] = rr["Do you consider yourself a member of the LGBT+ community?"].apply(lambda x: bitExtractor[x])
    cd["continent"] = rr["On what continent do you reside?"]
    cd["gmtOffset"] = rr["Using only its 3- to 4-letter abbreviation, what timezone are you in?"].apply(lambda x: getGMT(x))
    cd["education"] = rr["What is your highest level of education?"].apply(lambda x: abbreviationsOne[x])
    cd["isStudent"] = rr["Are you currently pursuing an education, either part- or full-time?"].apply(lambda x: bitExtractor[x])
    cd["employmentStatus"] = rr["Which of the following best describes your current employment status?"].apply(lambda x: abbreviationsOne[x])
    cd["weeklyConsFreq"] = rr["In an average week, on how many days do you watch anime, read manga, doujin or light novels, or play visual novels?"]
    cd["sociallyAnxious"] = rr["Have you ever suffered from social anxiety?"].apply(lambda x: bitExtractor[x])
    cd["consumptionSources"] = rr["Which of the following do you consume? Check all that apply. "]
    cd["platform"] = rr["How do you typically access anime?"].apply(lambda x: abbreviationsOne[x])
    cd["isPayer"] = rr["Have you ever held a paid subscription to an anime-focused streaming service such as VRV, Crunchyroll, or Funimation?"].apply(lambda x: bitExtractor[x])
    cd["prefersSubs"] = rr["When you watch anime, do you prefer subs or dubs?"].apply(lambda x: bitExtractor[x])
    cd["visQuality"] = rr["When choosing an anime, manga, LN, or VN, how important do you weigh visual qualities such as style, character design, and backgrounds?"]
    cd["storyQuality"] = rr["When choosing an anime, manga, or LN, how important do you weigh storytelling qualities such as dialogue, character development, and conflict?"]
    cd["characterRelatability"] = rr["When choosing an anime, manga, or LN, how important do you weigh character relatability?"]
    cd["firstFavGenre"] = rr["What genre do you most enjoy the most?"].apply(lambda x: abbreviationsOne[x])
    cd["secondFavGenre"] = rr["What genre do you most enjoy second-most?"].apply(lambda x: abbreviationsOne[x])
    cd["vTuberSub"] = rr["Have you ever considered subscribing to a VTuber?"].apply(lambda x: bitExtractor[x])
    cd["consumesHMat"] = rr["In the last month, have you consumed an H [adult] anime, manga, doujin, light, or a visual novel?"].apply(lambda x: bitExtractor[x])
    cd["socInc"] = rr["Do you think anime, manga, or the like could benefit from the better representation of certain social groups?"]
    cd["wantsMoreSeinen"] = rr["Were there more stories available for older, more mature audiences, would you consider reading or watching them?"].apply(lambda x: bitExtractor[x])


    # Machine-Readable Data.csv will...
    #   * Do everything Clean Data.csv does
    #   * Represent multiclass categorical variables with dummy variables

    mcCatKeys = ["gender", "continent", "education", "employmentStatus", "consumptionSources",
                "platform", "firstFavGenre", "secondFavGenre", "socInc"]
    # ^ Col keys to multiclass categorical variables ^
    numericVars = cd.drop(mcCatKeys, axis=1)
    # Get dummy variables
    gender = pd.get_dummies(cd["gender"])
    continents = pd.get_dummies(rr["On what continent do you reside?"].apply(lambda x: abbreviationsTwo[x]))
    education = pd.get_dummies(rr["What is your highest level of education?"].apply(lambda x: abbreviationsTwo[x]))
    employment = pd.get_dummies(rr["Which of the following best describes your current employment status?"].apply(
        lambda x: abbreviationsTwo[x]))
    consumptionSources = getConsumptionSources(rr["Which of the following do you consume? Check all that apply. "])
    platforms = pd.get_dummies(rr["How do you typically access anime?"].apply(lambda x: abbreviationsTwo[x]))
    firstFavGenre = pd.get_dummies(rr["What genre do you most enjoy the most?"]).rename(columns=genre_one)
    secondFavGenre = pd.get_dummies(rr["What genre do you most enjoy second-most?"]).rename(columns=genre_two)
    overH = pd.get_dummies(rr["Have you ever watched/read an anime, manga, doujin, LN, or VN, and felt the characters or story were cheapened through over-sexualization?"]).rename(
        columns=overH_ans)
    socialInclusion = pd.get_dummies(rr["Do you think anime, manga, or the like could benefit from the better representation of certain social groups?"]).rename(
        columns=inclusivity)
    # Concatenate results
    mrd = pd.concat([numericVars, gender, continents, education, employment, consumptionSources, platforms, firstFavGenre, secondFavGenre, overH, socialInclusion], axis=1)

    # Drop null entries and output files
    cd.dropna(inplace=True)
    cd.to_csv("Clean Data.csv")
    mrd.dropna(inplace=True)
    mrd.to_csv("Machine-Readable Data.csv")
