import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = int(input('Would you like to see data from Chicago (1), New York (2), or Washington(3)?: '))
        except ValueError:
            print('**Oops, please select from the following options - 1, 2, or 3**')
            continue
        if city not in (1, 2, 3):
            print('**Oops, please select from the following options - 1, 2, or 3**')
            continue
        else:
            break        
            
    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = int(input('Which month - January (1), February (2), March (3), April (4), May (5), June (6), or all (7)?: '))
        except ValueError:
            print('**Oops, please select from the following options - 1, 2, 3, 4, 5, 6, 7**')
        if month not in (1, 2, 3, 4, 5, 6, 7):
            print('**Oops, please select from the following options - 1, 2, 3, 4, 5, 6, 7**')      
        else:
            break
       
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = int(input('Which day - Monday (0), Tuesday (1), Wednesday (2), Thursday (3), Friday(4), Saturday (5), Sunday (6), or all (7): '))
        except ValueError:
            print('**Oops, please select from the following options - 0, 1, 2, 3, 4, 5, 6, 7**')
        if day not in (0, 1, 2, 3, 4, 5, 6, 7):
            print('**Oops, please select from the following options - 0, 1, 2, 3, 4, 5, 6, 7**')    
        else:
            break
        
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
   # convert integer input to city name
    if city == 1:
        city_name = "chicago"
    elif city == 2:
        city_name = "new york city"
    else:
        city_name = "washington"
    
   # convert integer input to day of week name

    if day == 0:
        day_name = "Monday"
    elif day == 1:
        day_name = "Tuesday"
    elif day == 2:
        day_name = "Wednesday"
    elif day == 3:
        day_name = "Thursday"
    elif day == 4:
        day_name = "Friday"
    elif day == 5:
        day_name = "Saturday"
    elif day == 6:
        day_name = "Sunday"
    else:
        day_name = 7
   
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city_name])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() #weekday_name may have been replaced for: day_name()


    # filter by month if applicable
    if month != 7:
         
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

        
    # filter by day of week if applicable
    if day_name != 7:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day_name] 
    
    return df


def time_stats(df, day, month):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month if all months selected
    if month == 7:
        print("The most popular month: {}".format(df['month'].mode()[0]))

    # display the most common day of week if all days selected
    if day == 7:
        print("The most common day of week: {}".format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    
    print("The most common start hour: {}".format(df['hour'].mode()[0]))

    print("\nThis took %.7s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common start station is: {}".format(df['Start Station'].mode()[0]))


    # display most commonly used end station
    print("The most common end station is: {}".format(df['End Station'].mode()[0]))


    # display most frequent combination of start station and end station trip     
    count_stations = df.groupby(['Start Station','End Station']).size().idxmax()
    
    print("The most common start and end station is: {}".format(count_stations))


    print("\nThis took %.7s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].sum()/3600
    print("Total travel time is: {:.1f} hours".format(travel_time))

    # display mean travel time
    travel_mean_time = df['Trip Duration'].mean()/60
    print("Average travel time is: {:.1f} minutes".format(travel_mean_time))

    print("\nThis took %.7s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("What is the breakdown of user types?\n{}\n".format(df['User Type'].value_counts()))


    # Display counts of gender
    
    if 'Gender' in df:
        print("What is the breakdown of gender?\n{}\n".format(df['Gender'].value_counts()))


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print("What is the earliest year of birth?\n{:.0f}".format(df['Birth Year'].min()))
        print("What is the most recent year of birth?\n{:.0f}".format(df['Birth Year'].max()))
        print("What is the most common year of birth?\n{:.0f}".format(df['Birth Year'].mode()[0]))
    
    print("\nThis took %.6s seconds." % (time.time() - start_time))
    print('-'*40)


def my_range(df):
    i = 0
    j = 5
  
    test = np.array(df)
    while j < len(df):
        yield test[i:j,:]
        i += 5
        j += 5

def display_data(df):
    i = 0
    j = 5
    
    while True:
         try:
             data_view = int(input('Would you like to the data? Yes (1), No (2): '))
         except ValueError:
            print('**Oops, please select from the following options - 1, or 2**')
            continue
         if data_view not in (1, 2):
            print('**Oops, please select from the following options - 1, or 2**')
            continue
    
         if data_view == 2:
            return
         if data_view == 1:
            print(df.iloc[i:j])
                      
            # data_view = input('Would you like to see more? Yes (1), No (2): ')
            i += 5
            j += 5 
                       

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, day, month)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        display_data(df)
                
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
