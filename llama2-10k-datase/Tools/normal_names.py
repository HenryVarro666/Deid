import csv

# 定义300个常规的英文名字
names = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Charles", "Joseph", "Thomas",
    "Christopher", "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew", "Kenneth",
    "Joshua", "Kevin", "Brian", "George", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan",
    "Jacob", "Gary", "Nicholas", "Eric", "Stephen", "Jonathan", "Larry", "Justin", "Scott", "Brandon",
    "Frank", "Benjamin", "Samuel", "Gregory", "Raymond", "Patrick", "Alexander", "Jack", "Dennis", "Jerry",
    "Harold", "Aaron", "Henry", "Douglas", "Peter", "Jesse", "Billy", "Jordan", "Albert", "Kyle",
    "Randy", "Louis", "Russell", "Carl", "Howard", "Fred", "Arthur", "Shawn", "Lawrence", "Joe",
    "Roy", "Ralph", "Philip", "Todd", "Danny", "Bryan", "Tony", "Sean", "Terry", "Gerald",
    "Keith", "Samuel", "Willie", "Ralph", "Lawrence", "Nicholas", "Roy", "Benjamin", "Bruce", "Brandon",
    "Adam", "Harry", "Fred", "Wayne", "Billy", "Steve", "Louis", "Jeremy", "Aaron", "Randy",
    "Howard", "Eugene", "Carlos", "Russell", "Bobby", "Victor", "Martin", "Ernest", "Phillip", "Craig",
    "Alan", "Shawn", "Clarence", "Sean", "Philip", "Chris", "Johnny", "Earl", "Jimmy", "Antonio",
    "Danny", "Bryan", "Tony", "Luis", "Mike", "Stanley", "Leonard", "Nate", "Dale", "Manuel",
    "Rodney", "Curtis", "Norman", "Allen", "Marvin", "Vincent", "Glenn", "Jeffery", "Travis", "Jeff",
    "Chad", "Jacob", "Lee", "Melvin", "Alfred", "Kyle", "Francis", "Bradley", "Jesus", "Herbert",
    "Frederick", "Ray", "Joel", "Edwin", "Don", "Eddie", "Ricky", "Troy", "Randall", "Barry",
    "Alexander", "Bernard", "Mario", "Leroy", "Francisco", "Marcus", "Micheal", "Theodore", "Clifford", "Miguel",
    "Oscar", "Jay", "Jim", "Tom", "Calvin", "Alex", "Jon", "Ronnie", "Bill", "Lloyd",
    "Tommy", "Leon", "Derek", "Warren", "Darrell", "Jerome", "Floyd", "Leo", "Alvin", "Tim",
    "Wesley", "Gordon", "Dean", "Ivan", "Caleb", "Bob", "Jaime", "Casey", "Alfredo", "Alberto",
    "Dave", "Ivan", "Johnnie", "Sidney", "Byron", "Julian", "Isaac", "Morris", "Clifton", "Willard",
    "Daryl", "Ross", "Virgil", "Andy", "Marshall", "Salvador", "Perry", "Kirk", "Sergio", "Marion",
    "Tracy", "Seth", "Kent", "Terrance", "Rene", "Eduardo", "Terrence", "Enrique", "Freddie", "Wade"
]

# # 将名字分割成多组，确保每组有300个名字
# name_chunks = [names[i:i + 300] for i in range(0, len(names), 300)]

# 将名字保存到CSV文件中
with open('normal_names.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for name in names:
        writer.writerow([name])



