import pandas as pd

# Dane wejściowe to wektor o długości 1000 w formacie *.csv.
# Mogą to być historyczne wartości indeksu WIG20, dane wzięte z giełdy walut FOREX itp.

set1 = pd.read_csv('wig20_d.csv').to_dict('list')
set2_df = pd.read_csv('wig20_d.csv', index_col='Data').Zamkniecie


def ema(data_list, span):
    alfa = 2 / (span + 1)
    ratio = 1 - alfa
    result = []

    for i in range(0, min(span, len(data_list))):
        numerator = 0
        denominator = 0
        mult = 1

        for day in range(0, i + 1):
            numerator += mult * data_list[i - day]
            denominator += mult
            mult *= ratio

        if (denominator != 0):
            result.append(numerator / denominator)

    denominator = (1 - (1 - alfa) ** (span + 1)) / alfa

    for i in range(span, len(data_list)):
        numerator = 0
        mult = 1

        for day in range(0, span + 1):
            numerator += mult * data_list[i - day]
            mult *= ratio

        result.append(numerator / denominator)

    return result


# returns values exactly like DataFrame.ewm(span = 2, adjust=True).mean()
def ema2(data_list, span):
    alfa = 2 / (span + 1)
    ratio = 1 - alfa
    result = []

    for i in range(0, len(data_list)):
        numerator = 0
        denominator = 0
        mult = 1

        for day in range(0, i + 1):
            numerator += mult * data_list[i - day]
            denominator += mult
            mult *= ratio

        if (denominator != 0):
            result.append(numerator / denominator)

    return result


# return the list: [macd, signal]
def macd_ind(data_list):
    ema12_list = ema(data_list, 12)
    ema26_list = ema(data_list, 26)
    macd_list = []

    for i in range(0, len(data_list)):
        macd_list.append(ema12_list[i] - ema26_list[i])

    signal_list = ema(macd_list, 9)

    return macd_list, signal_list


# takes the primary capital and counts the profit
# after following MACD indicator guideline
def macd_profit(capital, data_list):
    macd1 = macd_ind(data)

    macd_list = macd1[0]  # macd
    signal_list = macd1[1]  # signal

    # Miejsce, w którym MACD przecina SIGNAL od dołu
    # jest sygnałem do zakupu akcji, a w którym przecina od góry,
    # jest sygnałem do sprzedaży akcji.

    actions = 0
    last_capital = capital  # gdyby dla danych gra kończyła się# kupnem akcji - zwracamy ostatnią wartość kapitału

    for i in range(1, len(macd_list)):
        # MACD rośnie
        if macd_list[i-1] < signal_list[i-1] \
                and macd_list[i] >= signal_list[i] and capital != 0:
            # kupujemy akcje
            last_capital = capital
            actions = capital / data_list[i]
            capital = 0

        # MACD maleje
        elif macd_list[i-1] > signal_list[i-1] \
                and macd_list[i] <= signal_list[i] and capital == 0:
            # sprzedajemy akcje
            capital = actions * data_list[i]
            actions = 0

    if capital == 0:
        capital = last_capital

    return capital


# takes the primary capital and counts the profit
# after following MACD indicator guideline with some modification
# in regard with function MACD_PROFIT(...)
def macd_profit_vol2(capital, data_list):
    macd1 = macd_ind(data)

    macd_list = macd1[0]  # macd
    signal_list = macd1[1]  # signal

    # Miejsce, w którym MACD przecina SIGNAL od dołu i dzieje się to dla ujemnych wartości
    # jest sygnałem do zakupu akcji, a w którym przecina od góry i dzieje się to dla dodatnich wartości
    # jest sygnałem do sprzedaży akcji.

    actions = 0
    last_capital = capital  # gdyby dla danych gra kończyła się# kupnem akcji - zwracamy ostatnią wartość kapitału

    for i in range(1, len(macd_list)):
        # MACD rośnie
        if macd_list[i-1] < signal_list[i-1] \
                and macd_list[i] >= signal_list[i] and capital != 0\
                and macd_list[i] < 0:
            # kupujemy akcje
            last_capital = capital
            actions = capital / data_list[i]
            capital = 0

        # MACD maleje
        elif macd_list[i-1] > signal_list[i-1] \
                and macd_list[i] <= signal_list[i] and capital == 0\
                and macd_list[i] > 0:
            # sprzedajemy akcje
            capital = actions * data_list[i]
            actions = 0

    if capital == 0:
        capital = last_capital

    return capital


data = set1['Zamkniecie']

money = 1000
print(money)

money = macd_profit(money, data)
print(money)

money = 1000
money = macd_profit_vol2(money, data)
print(money)
