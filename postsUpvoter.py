import praw
import prawcore
import time as t

print("Bot name: postsUpvoter")
print("Desc: Upvotes the top posts in the new section. Limit of top posts")
print("is set by user.")
print()
print("::Warning:: A high post limit can take too much time")
print("            and can return error in some cases.")
print()
l = int(input("Enter the post limit(general is 10): "))

reddit = praw.Reddit('postsUpvoter')

print()
print("Selecting the followed subreddits from subbedSubReddits.txt")
print("file from the same directory...")
print()

textRead = open(r"subbedSubReddits.txt", "r")

with open("subbedSubReddits.txt") as f:  # extract the subbreddit listed in file
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
# remove '\n' after their name and return as a list
content = [x.strip('\n') for x in content]
# transfer the list to working variable while filtering the None datatype
mySubReddits = list(filter(None, content))
textRead.close()


def upvote():  # an author defined function which returns the upvote for post upvote
    return 'upvote'


time = 0  # used to record time
actions = 0  # checks number of upvotes/actions performed currently

# bot's posts upvoting body
for subreddits in mySubReddits:  # select subreddit 1 by 1 from the list
    # the subreddit has beeen selected to work upon further
    selected = reddit.subreddit(subreddits)
    print("Opened: r/", subreddits)
    # We will also look for pinned posts since some are old and cant be upvoted
    add = 0  # this variable stores no. of pinned posts at top

    for checkSticky in selected.new():
        if checkSticky.stickied == True:  # if post is a pinned one
            add += 1  # then add a number
        else:  # when encounter a non-pinned post
            break # we break this loop because we passed the pinned post list
    print("Pinned posts: ", add)

    # l+add stores the post limit and no. of pinned posts,
    # since we dont want to deal with pinned ones but they are added to
    # the number of posts visited
    print("Excluding pinnedd posts(if any) and upvoting the top posts...")

    time = t.time()  # records current timestamp to know time passed

    for posts in selected.new(limit=l+add):
        # we will now go through pinned post+normal post
        # and just upvote the normal ones now
        if posts.stickied == False:  # if post isn't pinned
            posts.upvote()  # upvote the post
            actions += 1 # add to the no. of actions performed on reddit
        t.sleep(2)
        # if we upvoted many posts in a short time we will wait to avoid getting
        # rejected by reddit as a spam
        if (t.time()-time) == 60 and actions == 55:  # checks if:
            # passed time to upvote the posts has been 60 sec
            # and number of actions are 55 and delays the program
            # check praw rules to know why this is done
            print("-------------------------------------------")
            print("Bot paused for 10 sec to avoid spam ban...")
            print("-------------------------------------------")
            t.sleep(10)

    actions = 0  # resets the num of actions performed
    print("Done with: r/", subreddits)
    print()

print("Bot has upvoted the posts.")
print("Exiting...")
