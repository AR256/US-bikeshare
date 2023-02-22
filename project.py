import time
import pandas as pd


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def check_data_entry(prompt, valid_entries):
    """
    Asks user to type some input and verify if the entry typed is valid.
    Since we have 3 inputs to ask the user in get_filters(), it is easier to write a function.
    Args:
        (str) prompt - message to display to the user
        (list) valid_entries - list of string that should be accepted
    Returns:
        (str) user_input - the user's valid input
    """
    try:
        user_input = str(input(prompt)).lower()

        while user_input not in valid_entries :
            print('Sorry... it seems like you\'re not typing a correct entry.')
            print('Let\'s try again!')
            user_input = str(input(prompt)).lower()

        print('Great! the chosen entry is: {}\n'.format(user_input))
        return user_input

    except:
        print('Seems like there is an issue with your input')



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hi there! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_cities = CITY_DATA.keys()
    prompt_cities = 'Please choose one of the 3 cities (chicago, new york city, washington): '
    city = check_data_entry(prompt_cities, valid_cities)


    # get user input for month (all, january, february, ... , june)
    valid_months = ['all','january','february','march','april','may','june']
    prompt_month = 'Please choose a month (all, january, february, ... , june): '
    month = check_data_entry(prompt_month, valid_months)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['all','monday','tuesday','wednesday','thursday','friday','saturday', 'sunday']
    prompt_day = 'Please choose a day (all, monday, tuesday, ... sunday): '
    day = check_data_entry(prompt_day, valid_days)


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    # load data file into a dataframe
    df = pd.read_csv(f'//workspaces//55091709//project//{CITY_DATA[city]}')

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Display the most common month
    print('most common month:', df['month'].mode()[0])

    #Display the most common day of week
    print('most common day of week:', df['day_of_week'].mode()[0])

    #Display the most common start hour
    print('most common start hour:', df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return f"{df['month'].mode()[0]}, {df['day_of_week'].mode()[0]}, {df['Start Time'].dt.hour.mode()[0]}"


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Display most commonly used start station
    print('most commonly used start station:', df['Start Station'].mode()[0])

    #Display most commonly used end station
    print('most commonly used end station:', df['End Station'].mode()[0])

    #Display most frequent combination of start station and end station trip
    df['Trips'] = df['Start Station'] + ' to ' + df['End Station']
    print('most frequent combination of start station and end station trip:',df["Trips"].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return f"{df['Start Station'].mode()[0]}, {df['End Station'].mode()[0]}"


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    print('total travel time:', df['Trip Duration'].sum())

    #display mean travel time
    print('mean travel time:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return f"{df['Trip Duration'].sum()}, {df['Trip Duration'].mean()}"

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    print('counts of user types:\n', df['User Type'].value_counts())
    try:
        #Display counts of gender
        print('counts of gender:\n', df['Gender'].value_counts())
    except KeyError:
        print('No available data for Gender')
    try:
        #Display earliest, most recent, and most common year of birth
        print('earliest, most recent, and most common year of birth:', df['Birth Year'].min(), df['Birth Year'].max(), df['Birth Year'].mode()[0])
    except KeyError:
        print('No available data for Birth Year')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return f"{df['Birth Year'].min()}, {df['Birth Year'].max()}, {df['Birth Year'].mode()[0]}"


def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower().strip()
    start_loc = 0
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower().strip()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
