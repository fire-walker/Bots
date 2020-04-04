import sys, discord, os, io, aiohttp, random, datetime
from random import randrange
from secrets import SystemRandom
from psutil import cpu_count
from multiprocessing.pool import ThreadPool
from discord.ext import commands

def sift_primes(primes_list, pc):
    for dp in primes_list:
        if pc % dp == 0:
            return False
    primes_list.append(pc)
    return True

def smallprimes(max = 65535):
    primes_list = [2,  3]
    i = 5
    while i <= max:
        sift_primes(primes_list, i)
        i += 2
    return primes_list

def is_prime(
n,
k=192,
def_list=[],
min_s=0,
totient_coprimes=[65537],
stop=[False]
):


    if min_s < 1 and n == 2:
        return True
    if min_s < 2 and n == 3:
        return True
    if n == 3:
        stop[0] = True
        return False
    if n <= 1 or n % 2 == 0:
        stop[0] = True
        return False

    for dp in totient_coprimes:
        if dp <= 2:
            continue
        if ( (min_s > 1) and ((1 << min_s) % dp ==0) ):
            continue
        if (n - 1) % dp == 0:
            stop[0] = True
            return False

    s = 0
    r = n - 1

    while r & 1 == 0:
        s += 1
        r //= 2
    
    if min_s > 0 and s < min_s:
        stop[0] = True
        return False

    for dp in def_list:

        if stop[0]:
            return False
        
        if dp >= n:
            return True
        if n % dp == 0:
            stop[0] = True
            return False

    if len(def_list) > 0:
        highest_known_prime = def_list[len(def_list) - 1]
        highest_known_prime *= highest_known_prime
        if n < highest_known_prime:
            return True
    
    odd_ones = 0

    n1 = (1 << 32) - 1
    for _ in range(k):
        
        if stop[0]:
            return False

        a = randrange(2, n - 1)
        
        if a > n1 + 1:
            a -= randrange(0,  n1)

        x = pow(a, r, n)
        
        if min_s != -1 and x == 1:
            odd_ones += 1
            if odd_ones == k:
                stop[0] = True
                return False

        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    stop[0] = True
                    return False
                j += 1
            if x != n - 1:
                stop[0] = True
                return False

    return True

def generate_prime_candidate(length,  rng,  min_s=0):

    maxint_v = 2
    maxint_s = 1
    while maxint_v < sys.maxsize:
        maxint_s += 1
        maxint_v = maxint_v << 1
    maxint_v -= 1

    min_s_mask = 0
    i = 1
    while i < min_s:
        min_s_mask |= 1 << i
        i += 1

    p = 0
    remainder = length % maxint_s

    for _ in range((length + maxint_s - 1) // maxint_s):
        p = p << maxint_s
        p += rng.randint(0,  maxint_v)

    if remainder > 0:
        p = p >> (maxint_s - remainder)

    if min_s > 1:
        p |= 1 << max(length - 1,  min_s)
        p -= 1 << min_s
        p |= min_s_mask
        p += 2

    p |= (1 << length - 1) | 1

    return p

def gen_prim_root(mod, t2):
    m = 1
    while True:
        m += 1
        if pow(m, 2, mod) == 1:
            continue
        if pow(m, t2, mod) == 1:
            continue
        return m

def generate_strong_prime(length=2048):

    if length < 3:
        return 7

    length_v = 1 << length

    rng = SystemRandom()
    
    min_s = 0

    p = generate_prime_candidate(length,  rng,  min_s) | 3
    
    def_list = smallprimes(4096)
    
    pool = ThreadPool()

    cores = (cpu_count(logical=True) // 2) - 1
    if cores < 1:
        cores = 1

    while True:
        
        stop_threads = []
        for i in range(cores):
            stop_threads.append([False])
        
        nums=[]
        inputs=[]

        for i in range(cores):
            p += 4
            if p >= length_v:
                p -= length_v >> 1
            p2 = p >> 1
            nums.append(p)
            inputs.append((p, 192, def_list, min_s,  [], stop_threads[i]))
            inputs.append((p2, 192, def_list, min_s,  [], stop_threads[i]))
        inputs.reverse() #assuming smallest results are prefered
        nums.reverse() #same here

        async_result = pool.starmap_async(is_prime,inputs)
        results = async_result.get()
        
        while len(results)!=0:
            res1=results.pop()
            res2=results.pop()
            res3=nums.pop()
            if res1 and res2:
                return res3
        

def main(size):
    input = sys.argv
    
    input1 = size
    if len(input) > 1:
        input1 = int(input[1])

    global g
    global n
    n = generate_strong_prime(input1)
    g = gen_prim_root(n, (n - 1) >> 1)





class primes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help = ".prime send/upload length")
    async def prime(self, ctx, method, size='2048'):
        meth = ['send', 'upload']
        if method not in meth:
            await ctx.send("Wrong syntax: `{}` is not a recognized intake" .format(method))
        else:
            global n
            global g

            await ctx.send("This may take a while..... or not, depends on your luck")

            someurl = ['https://media.giphy.com/media/xTkcEQACH24SMPxIQg/giphy.gif',
                    'https://media.giphy.com/media/26tPcVAWvlzRQtsLS/giphy.gif',
                    'https://media.giphy.com/media/oQxxiAx3EzaU0/giphy.gif',
                    'https://media.giphy.com/media/2TogQ5TvjnsrK/giphy.gif',
                    'https://media.giphy.com/media/4yvWqqCSlp2I8/giphy.gif',
                    'https://media.giphy.com/media/EIyuzZk6IDUMU/giphy.gif'
                    ]
            async with aiohttp.ClientSession() as session:
                async with session.get(random.choice(someurl)) as resp:
                    if resp.status != 200:
                        return await ctx.channel.send('Could not load file...')
                    data = io.BytesIO(await resp.read())
                    await ctx.channel.send(file=discord.File(data, 'image.gif'))

            size = int(size)
            if size == 1:
                size = 512
            if size == 2:
                size = 1024
            if size == 3:
                size = 2048
            if size == 4:
                size = 4096
            main(size)

            if method == "send":
                embed = discord.Embed(title="Generator", description='```{}```' .format(g), colour=discord.Colour(0x41bbc6), timestamp=datetime.datetime.utcfromtimestamp(1575115023))
                embed.set_footer(text="generated")
                await ctx.send(embed=embed)

                embed = discord.Embed(title="Prime Number", description="```{}```" .format(n), colour=discord.Colour(0xc64170), timestamp=datetime.datetime.utcfromtimestamp(1575115023))
                embed.set_footer(text="generated")
                await ctx.send(embed=embed)
            
            if method == "upload":
                with open('keys.txt', 'w') as file:
                    file.write("{0} : {1}" .format(g, n))
                
                with open('keys.txt', 'rb') as fff:
                    await ctx.channel.send(file=discord.File(fff, 'keys.txt'))
                
                os.remove('keys.txt')
        



def setup(bot):
    bot.add_cog(primes(bot))
