from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

YEAR_CHOICES = (
    ("1900", "1900"),
    ("1901", "1901"),
    ("1902", "1902"),
    ("1903", "1903"),
    ("1904", "1904"),
    ("1905", "1905"),
    ("1906", "1906"),
    ("1907", "1907"),
    ("1908", "1908"),
    ("1909", "1909"),
    ("1910", "1910"),
    ("1911", "1911"),
    ("1912", "1912"),
    ("1913", "1913"),
    ("1914", "1914"),
    ("1915", "1915"),
    ("1916", "1916"),
    ("1917", "1917"),
    ("1918", "1918"),
    ("1919", "1919"),
    ("1920", "1920"),
    ("1921", "1921"),
    ("1922", "1922"),
    ("1923", "1923"),
    ("1924", "1924"),
    ("1925", "1925"),
    ("1926", "1926"),
    ("1927", "1927"),
    ("1928", "1928"),
    ("1929", "1929"),
    ("1930", "1930"),
    ("1931", "1931"),
    ("1932", "1932"),
    ("1933", "1933"),
    ("1934", "1934"),
    ("1935", "1935"),
    ("1936", "1936"),
    ("1937", "1937"),
    ("1938", "1938"),
    ("1939", "1939"),
    ("1940", "1940"),
    ("1941", "1941"),
    ("1942", "1942"),
    ("1943", "1943"),
    ("1944", "1944"),
    ("1945", "1945"),
    ("1946", "1946"),
    ("1947", "1947"),
    ("1948", "1948"),
    ("1949", "1949"),
    ("1950", "1950"),
    ("1951", "1951"),
    ("1952", "1952"),
    ("1953", "1953"),
    ("1954", "1954"),
    ("1955", "1955"),
    ("1956", "1956"),
    ("1957", "1957"),
    ("1958", "1958"),
    ("1959", "1959"),
    ("1960", "1960"),
    ("1961", "1961"),
    ("1962", "1962"),
    ("1963", "1963"),
    ("1964", "1964"),
    ("1965", "1965"),
    ("1966", "1966"),
    ("1967", "1967"),
    ("1968", "1968"),
    ("1969", "1969"),
    ("1970", "1970"),
    ("1971", "1971"),
    ("1972", "1972"),
    ("1973", "1973"),
    ("1974", "1974"),
    ("1975", "1975"),
    ("1976", "1976"),
    ("1977", "1977"),
    ("1978", "1978"),
    ("1979", "1979"),
    ("1980", "1980"),
    ("1981", "1981"),
    ("1982", "1982"),
    ("1983", "1983"),
    ("1984", "1984"),
    ("1985", "1985"),
    ("1986", "1986"),
    ("1987", "1987"),
    ("1988", "1988"),
    ("1989", "1989"),
    ("1990", "1990"),
    ("1991", "1991"),
    ("1992", "1992"),
    ("1993", "1993"),
    ("1994", "1994"),
    ("1995", "1995"),
    ("1996", "1996"),
    ("1997", "1997"),
    ("1998", "1998"),
    ("1999", "1999"),
    ("2000", "2000"),
    ("2001", "2001"),
    ("2002", "2002"),
    ("2003", "2003"),
    ("2004", "2004"),
    ("2005", "2005"),
    ("2006", "2006"),
    ("2007", "2007"),
    ("2008", "2008"),
    ("2009", "2009"),
    ("2010", "2010"),
    ("2011", "2011"),
    ("2012", "2012"),
    ("2013", "2013"),
    ("2014", "2014"),
    ("2015", "2015"),
    ("2016", "2016"),
    ("2017", "2017"),
    ("2018", "2018"),
    ("2019", "2019"),
    ("2020", "2020"),
    ("2021", "2021"),
    ("2022", "2022"),
    ("2023", "2023"),
    ("2024", "2024"),
    ("2025", "2025"),
    ("2026", "2026"),
    ("2027", "2027"),
    ("2028", "2028"),
    ("2029", "2029"),
    ("2030", "2030"),
    ("2031", "2031"),
    ("2032", "2032"),
    ("2033", "2033"),
    ("2034", "2034"),
    ("2035", "2035"),
    ("2036", "2036"),
    ("2037", "2037"),
    ("2038", "2038"),
    ("2039", "2039"),
    ("2040", "2040"),
    ("2041", "2041"),
    ("2042", "2042"),
    ("2043", "2043"),
    ("2044", "2044"),
    ("2045", "2045"),
    ("2046", "2046"),
    ("2047", "2047"),
    ("2048", "2048"),
    ("2049", "2049"),
    ("2050", "2050"),
    ("2051", "2051"),
    ("2052", "2052"),
    ("2053", "2053"),
    ("2054", "2054"),
    ("2055", "2055"),
    ("2056", "2056"),
    ("2057", "2057"),
    ("2058", "2058"),
    ("2059", "2059"),
    ("2060", "2060"),
    ("2061", "2061"),
    ("2062", "2062"),
    ("2063", "2063"),
    ("2064", "2064"),
    ("2065", "2065"),
    ("2066", "2066"),
    ("2067", "2067"),
    ("2068", "2068"),
    ("2069", "2069"),
    ("2070", "2070"),
    ("2071", "2071"),
    ("2072", "2072"),
    ("2073", "2073"),
    ("2074", "2074"),
    ("2075", "2075"),
    ("2076", "2076"),
    ("2077", "2077"),
    ("2078", "2078"),
    ("2079", "2079"),
    ("2080", "2080"),
    ("2081", "2081"),
    ("2082", "2082"),
    ("2083", "2083"),
    ("2084", "2084"),
    ("2085", "2085"),
    ("2086", "2086"),
    ("2087", "2087"),
    ("2088", "2088"),
    ("2089", "2089"),
)


class StockTicker(models.Model):
    STOCK_TYPE_CHOICES = (
        ("INDIVIDUAL", "Individual"),
        ("INDEX_FUND/EFT", "Index Fund/EFT"),
    )
    STOCK_CATEGORY_CHOICES = (
        ("EQUITIES", "Equities"),
        ("BONDS", "Bonds"),
        ("CASH_AND_CASH_EQUIVALENT", "Cash and Cash Equivalents"),
        ("DIVERSIFIED", "Diversified"),
        ("REITS", "Reits"),
        ("OTHERS", "Others"),
    )
    name = models.CharField(
        max_length=50,
    )
    ticker = models.CharField(
        max_length=50,
    )
    stock_type = models.CharField(
        choices=STOCK_TYPE_CHOICES, max_length=100, null=False, blank=False
    )
    stock_category = models.CharField(
        choices=STOCK_CATEGORY_CHOICES, max_length=100, null=True, blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f"{self.name} ({self.ticker})"

    class Meta:
        unique_together = (('ticker', 'user'),)


class Stock(models.Model):
    stock_ticker = models.ForeignKey(StockTicker, on_delete=models.CASCADE, blank=False, null=False)
    quantity = models.FloatField(
        null=False, blank=False, default=0.0,
    )
    investment = models.FloatField(
        null=False, blank=False, default=0.0,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    year = models.CharField(choices=YEAR_CHOICES, null=False, blank=False, max_length=4)

    class Meta:
        unique_together = ('user', 'stock_ticker', 'year')

    def __str__(self):
        return f"{self.stock_ticker.name} ({self.year})"


class StockTransaction(models.Model):
    TRANSACTION_TYPE_SOURCES = (
        ("Buy", "Buy"),
        ("Sell", "Sell"),
    )
    stock_ticker = models.ForeignKey(StockTicker, on_delete=models.CASCADE, blank=False, null=False)
    transaction_type = models.CharField(
        choices=TRANSACTION_TYPE_SOURCES, max_length=100, null=False, blank=False
    )
    quantity = models.FloatField(
        blank=False, default=0.0,
    )
    spot_price = models.FloatField(
        blank=False, null=False, default=0.0
    )
    date = models.DateField(null=True, blank=True, default=now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f"{self.stock_ticker} - {self.transaction_type}"
