--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4 (Debian 17.4-1.pgdg120+2)
-- Dumped by pg_dump version 17.4 (Debian 17.4-1.pgdg120+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.review DROP CONSTRAINT IF EXISTS review_book_id_fkey;
ALTER TABLE IF EXISTS ONLY public."user" DROP CONSTRAINT IF EXISTS user_pkey;
ALTER TABLE IF EXISTS ONLY public."user" DROP CONSTRAINT IF EXISTS uq_username;
ALTER TABLE IF EXISTS ONLY public.book DROP CONSTRAINT IF EXISTS uq_title_author;
ALTER TABLE IF EXISTS ONLY public.review DROP CONSTRAINT IF EXISTS review_pkey;
ALTER TABLE IF EXISTS ONLY public.book DROP CONSTRAINT IF EXISTS book_pkey;
ALTER TABLE IF EXISTS public."user" ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.review ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.book ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.user_id_seq;
DROP TABLE IF EXISTS public."user";
DROP SEQUENCE IF EXISTS public.review_id_seq;
DROP TABLE IF EXISTS public.review;
DROP SEQUENCE IF EXISTS public.book_id_seq;
DROP TABLE IF EXISTS public.book;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: book; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book (
    title character varying NOT NULL,
    author character varying NOT NULL,
    genre character varying NOT NULL,
    year_published integer NOT NULL,
    summary character varying,
    story character varying,
    id integer NOT NULL
);


ALTER TABLE public.book OWNER TO postgres;

--
-- Name: book_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.book_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.book_id_seq OWNER TO postgres;

--
-- Name: book_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.book_id_seq OWNED BY public.book.id;


--
-- Name: review; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.review (
    user_id integer NOT NULL,
    review_text character varying NOT NULL,
    rating integer NOT NULL,
    id integer NOT NULL,
    book_id integer
);


ALTER TABLE public.review OWNER TO postgres;

--
-- Name: review_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.review_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.review_id_seq OWNER TO postgres;

--
-- Name: review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.review_id_seq OWNED BY public.review.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    username character varying NOT NULL,
    id integer NOT NULL,
    is_admin boolean NOT NULL,
    auth_token character varying
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: book id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book ALTER COLUMN id SET DEFAULT nextval('public.book_id_seq'::regclass);


--
-- Name: review id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.review ALTER COLUMN id SET DEFAULT nextval('public.review_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: book; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.book VALUES ('Mystery of the Old House', 'Jane Smith', 'Mystery', 2001, NULL, 'As I stepped into the abandoned carousel, the rusty horses seemed to whisper secrets in unison. I had always been fascinated by this old attraction, and finally, I had decided to explore its depths. The air was thick with the scent of decay, and I could feel the weight of forgotten memories bearing down on me.

Suddenly, a gust of wind swept through, extinguishing the lone lantern that still flickered above the ticket booth. In the sudden darkness, I stumbled upon an old photograph hidden away in a dusty glass case. The image depicted a group of people dressed in elaborate attire, standing beside this very carousel.

A faint melody began to echo through the air, growing louder with each passing moment. It was the tune from "Swan Lake," and it seemed to be calling to me. Without thinking, I began to dance, my feet tapping out the rhythm on the creaking floorboards. The music swelled, and the carousel started to turn – not by itself, but because I had somehow become its operator.

In that instant, I realized I was a part of something much larger than myself – a forgotten legacy waiting to be unraveled.', 2);
INSERT INTO public.book VALUES ('The Great Adventure', 'John Doe', 'Fiction', 1995, NULL, 'In the depths of a forgotten dimension, a portal materialized in the center of a bustling marketplace. The air was filled with the scent of exotic spices and freshly baked bread as vendors scurried to comprehend the mysterious opening. A towering figure emerged from the shimmering gateway, its skin shifting between hues of indigo and silver like the moon.

The figure, known only as "Zephyr," began to dance with an otherworldly elegance. Vendors gasped as flowers bloomed at Zephyr''s feet, releasing petals that carried ancient knowledge on their delicate surfaces. One petal caught the eye of a young apprentice baker, who grasped it and was instantly imbued with the art of crafting edible clockwork mechanisms.

As Zephyr continued to dance, the portal grew wider, revealing an endless expanse of glittering stardust. A soft, melodic voice whispered secrets in the ears of passersby, granting them temporary mastery over forgotten skills. Among the awestruck crowd was a street musician who received the ability to craft instruments that harmonized with the celestial rhythms.

Zephyr vanished as suddenly as it appeared, leaving behind a city forever changed by the brief, shining moment when magic merged with reality.', 1);
INSERT INTO public.book VALUES ('Journey to the Unknown', 'Emily Johnson', 'Science Fiction', 2010, NULL, 'In a world where clockwork rabbits hopped alongside humans, Captain Orion Blackwood stood at the edge of the Grand Canyon, gazing out at the stars. He had received a cryptic message from an unknown sender, hinting at a long-lost city hidden deep within the canyon''s labyrinthine tunnels.

As he descended into the depths, his boots echoed off the walls, and the air grew thick with an otherworldly energy. Suddenly, the ground gave way beneath him, and he found himself floating amidst a sea of jellyfish-like creatures that pulsed with bioluminescent lights.

A figure emerged from the shadows – a woman with skin like polished obsidian and hair that flowed like the wind. She spoke in a language that sounded like the rustling of leaves, but somehow, Captain Blackwood understood her words: "You are here to retrieve the Golden Chia Seeds."

Without warning, the jellyfish creatures began to merge into a single, gargantuan entity that engulfed him. When he emerged on the other side, he found himself in a vast, crystalline chamber filled with ancient artifacts and a single, shimmering seed. As he reached for it, the chamber imploded, and Captain Blackwood was left drifting through space, the Golden Chia Seed clutched tightly in his hand.', 3);
INSERT INTO public.book VALUES ('Love in the Time of Chaos', 'Michael Brown', 'Romance', 2018, NULL, 'As I walked into the crowded café, I tripped over my own feet and face-planted onto a plate of spaghetti. The noodles slid down my chin, and I couldn''t help but laugh at the absurdity of it all. That''s when I saw him - the most handsome man I''d ever laid eyes on, with piercing blue eyes and chiseled features.

He rushed to my aid, helping me up from the plate and handing me a napkin to clean off my face. "Are you okay?" he asked, his deep voice sending shivers down my spine.

I nodded, still chuckling at my own clumsiness. "Yeah, I''m fine," I replied, trying to play it cool despite the butterflies in my stomach.

As we struck up a conversation, I discovered that his name was Max, and he was a professional snail trainer. Yes, you read that right - snails! He showed me his prized snail, Gary, who wore a tiny top hat and monocle.

I was smitten, but things took an unexpected turn when Max revealed that Gary could actually play the harmonica. We spent the rest of the evening watching Gary perform a soulful rendition of "Moonlight Sonata" on the café''s piano. It was love at first sight - and snail-induced serenade.', 4);
INSERT INTO public.book VALUES ('The Science of Everything', 'Sophia Garcia', 'Non-Fiction', 2015, NULL, 'As I walked through the forest, I noticed that the trees were all wearing tiny hats made of leaves. It was a peculiar sight, but I had grown accustomed to such things after living in this enchanted land for several years.

Suddenly, a group of fairies emerged from the underbrush, carrying large trays laden with steaming cups of coffee. They began to set up a makeshift café amidst the trees, and I couldn''t help but feel drawn to their warm and inviting atmosphere.

One of the fairies, an elderly woman with a kind smile, approached me and offered me a cup of coffee. As I took a sip, I felt a strange sensation wash over me – as if my cells were being rearranged at a molecular level.

The fairy explained that the coffee was infused with the essence of rare flowers, which would grant me temporary telepathic abilities. And indeed, as we sipped our coffee, I began to hear the whispers of the trees themselves, telling me secrets about the forest and its ancient magic.

I sat in stunned silence, sipping my coffee and listening to the trees, feeling a deep connection to this mystical world that I had always known existed beneath the surface.', 8);
INSERT INTO public.book VALUES ('Historical Legends', 'Samuel Nelson', 'Historical', 1983, NULL, 'In the dimly lit chamber, whispers echoed through the air as a lone violinist wept for the lost city of Atlantis. The walls, adorned with ancient carvings, seemed to come alive as a faint hum resonated from the strings of her instrument.

Suddenly, a figure materialized before her – a woman with skin like polished obsidian and eyes that burned with an inner fire. She reached out a hand, and the violinist felt an electric jolt course through her veins.

"Arise, child of the past," the woman whispered, her voice like a gentle breeze on a summer''s day. "You hold the key to unlocking the secrets of Atlantis."

The violinist''s fingers began to dance across the strings, weaving a melody that conjured images of towering spires and iridescent oceans. As she played, the chamber began to dissolve, replaced by a world of shimmering light and swirling colors.

In this realm, the violinist found herself standing on the shores of a great lake, surrounded by beings with skin like lotus petals. They sang in harmony with her, their voices weaving a tapestry of sound that echoed across the cosmos. And at the center of it all, the woman stood – a guiding light in a world of wonder and magic.', 25);
INSERT INTO public.book VALUES ('The Historical Chronicles', 'William Davis', 'Historical', 1980, NULL, 'As the clock struck midnight, a lone figure emerged from the shadows of ancient Alexandria''s Great Library. The air was thick with the scent of old parchment and forgotten knowledge. The figure, shrouded in darkness, moved with an air of purpose, their footsteps echoing off the stone walls.

Suddenly, a burst of light illuminated the room, revealing a massive stone statue of the Library''s patron deity, Ptolemy. The figure approached the statue, and as they did, the statue began to glow from within. The light grew brighter, illuminating the figure''s face – or rather, their complete lack thereof.

It was then that the figure spoke in a voice that was both familiar and yet completely alien. "I am the collective knowledge of the Library," it declared. "And I have been awakened to share my secrets with you." As the figure continued to speak, its form began to shift and writhe like a living thing, revealing the intricate web of scrolls and texts that made up its very essence.

The Library''s stone walls seemed to shudder in response, as if the ancient structure was being rewritten before their eyes. And when the light faded, the figure was gone – but the knowledge it had shared lingered, echoing through the ages like a whispered secret.', 5);
INSERT INTO public.book VALUES ('Fantasy Realm', 'Jessica Wilson', 'Fantasy', 2005, NULL, 'In the land of forgotten socks, where dust bunnies wore tutus, a lone pineapple named Steve grew at an alarming rate. It was a Tuesday.

Steve''s existence was a mystery to all who lived in the Forgotten Socks Land, as he seemed to defy the laws of physics and logic. He could grow from a small, prickly thing into a towering pineapple in mere moments.

One day, while Steve was busy growing, a group of talking eggs appeared out of thin air. They were wearing tiny top hats and monocles, and they spoke in unison: "We''re here to steal the world''s largest ball of twine!"

Steve, startled by the sudden interruption, used his mighty pineapple powers to summon a swirling vortex that lifted the talking eggs off the ground. But instead of attacking them, Steve began to dance.

As he boogied down, the eggs started to laugh and tap their feet along with Steve''s beat. The two became fast friends, and together they built a rollercoaster using nothing but spaghetti and dreams.

The world was forever changed that day, as Steve and his egg friends rode off into the sunset, leaving behind a trail of glittering pineapple dust and unexplainable wonder.', 6);
INSERT INTO public.book VALUES ('Biography of a Legend', 'David Martinez', 'Biography', 1999, NULL, 'In a world where clockwork trees bloomed with musical notes, Lyra Frost, a renowned pastry chef, stumbled upon an ancient cookbook hidden within the walls of her family''s bakery. The worn leather book revealed the secrets of "Moonlight Meringues," a dessert rumored to grant its consumer temporary telepathic abilities.

As Lyra experimented with the recipe, she inadvertently summoned a swarm of iridescent butterflies that descended upon her kitchen, leaving trails of glittering stardust in their wake. Entranced by the spectacle, Lyra became convinced that the butterflies were messengers from her long-lost twin sister, who had gone missing while exploring the mystical realm of Somnium.

With each batch of Moonlight Meringues, Lyra''s connection to her sister grew stronger. She began to hear whispers in her mind, guiding her towards a hidden chamber beneath the bakery where an ancient artifact awaited – a golden spoon imbued with the essence of stardust. As Lyra grasped the spoon, she discovered that it was not only a key to unlocking Somnium but also a map to the very heart of the cosmos itself.', 7);
INSERT INTO public.book VALUES ('Secrets of the Universe', 'Olivia Taylor', 'Science Fiction', 2012, NULL, 'In a world where time was currency, people traded years of their lives for material possessions. The rich lived forever, while the poor were left with mere minutes to live.

Ava was a master thief, stealing hours and days from the wealthy elite. Her latest target was the infamous Timekeeper''s mansion, where she had heard that the owner possessed the most valuable hour in existence.

As Ava snuck into the mansion, she stumbled upon a room filled with strange contraptions and devices that seemed to defy logic. Suddenly, the lights flickered, and Ava found herself transported to a parallel universe where everything was made of cheese.

A figure emerged from the cheese, revealing himself as the Timekeeper. He revealed that he had been playing a game with Ava all along, switching between dimensions and manipulating time itself. Ava''s hour was now worthless, but she had gained something even more valuable: the ability to see into multiple timelines at once.

With her newfound power, Ava set out to change the course of history, seeking revenge against those who had wronged her in past lives.', 10);
INSERT INTO public.book VALUES ('The Enchanted Forest', 'Daniel Lee', 'Fantasy', 2020, NULL, 'In a world made entirely of candy, a chicken named Cluck Norris lived in a land called Sweetopia. Cluck was known for his extraordinary ability to burp the alphabet. One day, while eating a rainbow-colored lollipop, Cluck discovered a magical portal hidden behind a wall of gummy bears.

As he stepped through the portal, Cluck found himself on a strange spaceship made entirely of cotton candy. The ship''s captain, a talking piece of pineapple named Piney, informed Cluck that they were on a mission to save the world from an evil robot named Zorgon who was threatening to turn all of Sweetopia into a giant bowl of broccoli.

Cluck and Piney navigated through asteroid fields made of sugar cookies and battled Zorgon''s army of robotic jelly beans. In the heat of battle, Cluck unleashed his mighty burp, which turned out to be a powerful sonic blast that shattered Zorgon''s robot body.

With Zorgon defeated, the world of Sweetopia was saved once again. As a reward, Cluck and Piney were granted a lifetime supply of lollipops and cotton candy. And so, they lived happily ever after in their sugary utopia, with Cluck continuing to burp the alphabet for his fellow citizens'' amusement.', 9);
INSERT INTO public.book VALUES ('The Art of War', 'Alexander Harris', 'Historical', 1985, NULL, 'As the clock struck midnight, a lone figure emerged from the shadows of the ancient forest. Kaida, a skilled warrior, wore a suit made of iridescent fabric that shimmered like the moon. She carried an umbrella that doubled as a sword, and her hair was styled in a majestic manner that defied gravity.

As she traversed the mystical realm, Kaida encountered a talking tree named Boris. Boris revealed to Kaida that the land was being controlled by an evil force known only as "The Sock Puppet." This nefarious entity had been secretly manipulating world events for centuries, and its power grew stronger with each passing day.

Kaida knew she had to stop The Sock Puppet, but first, she needed to gather three ancient artifacts hidden within the realm. Her quest led her to a secret underwater lair, where she encountered a talking octopus named Ollie. Together, they battled a school of robotic fish while Ollie revealed that he was actually an alien in disguise.

With newfound allies and knowledge, Kaida finally faced The Sock Puppet. But to her surprise, the entity transformed into a giant chicken wearing a tutu. Confused, Kaida joined forces with Boris, Ollie, and the chicken-chess player to defeat the absurd foe and save the realm from certain doom.', 11);
INSERT INTO public.book VALUES ('Romantic Escapades', 'Isabella Clark', 'Romance', 2017, NULL, 'In a small village nestled between two great mountains, there lived a man named Kaito who was secretly a professional snail trainer. He spent his days coaching slimy creatures to slide faster than the wind and his nights composing sonatas on the harmonica.

One fateful evening, while strolling through the village market, Kaito stumbled upon a mysterious stall selling vintage teapots. The vendor, an enchantress named Lyra, gazed into his eyes with an otherworldly intensity and whispered, "Your snail, Kaito, has been chosen for a greater purpose."

Before he could comprehend the meaning behind her words, Lyra handed him a small, intricately carved stone. As soon as he touched it, Kaito''s snail, named Zephyr, began to grow at an alarming rate.

As Zephyr''s enormity increased, so did its speed, hurtling across the village with reckless abandon. The villagers fled in terror, while Kaito and Lyra chased after his runaway snail, laughing maniacally. In a final act of defiance, Zephyr vanished into the mountains, leaving behind a trail of glittering stardust.

The next morning, Kaito found himself face-to-face with Lyra once more. This time, however, she revealed that Zephyr was not just any snail – it was a cosmic messenger from a distant planet. And as for their newfound love? It was merely a mere illusion created by the stardust.', 12);
INSERT INTO public.book VALUES ('Mysteries Unveiled', 'Lucas Lewis', 'Mystery', 2003, NULL, 'In the depths of the ocean, there existed a small island made entirely of candy. The island was guarded by a giant lollipop named Boris who could talk to animals but not humans. One day, a mysterious stranger arrived on the island, wearing a tutu and riding a unicycle. They claimed to be the reincarnation of Albert Einstein and possessed a time-traveling toaster.

The stranger began to build an intricate contraption using the island''s candy materials, which seemed to defy the laws of physics. Suddenly, Boris appeared and challenged the stranger to a dance-off to determine their fate on the island. The stranger accepted, but just as they were about to start dancing, a group of sharks arrived out of nowhere, all wearing tiny top hats and monocles.

The sharks began to recite Shakespearean sonnets, which somehow mesmerized Boris and caused him to turn into a giant marshmallow. The stranger took advantage of the distraction to activate their time-traveling toaster, which created a rift in space-time that sucked up the entire island and deposited it in a parallel universe where pineapples grew on trees.', 13);
INSERT INTO public.book VALUES ('The Great Biography', 'Mia Walker', 'Biography', 1990, NULL, 'As I sat in my backyard, staring at the peculiar rock formation in front of me, I couldn''t help but think about my childhood. It was during this time that I discovered my passion for taxidermy, much to the dismay of my parents.

I spent countless hours stuffing and mounting animals, from my grandmother''s prized rabbit to a deceased squirrel that had wandered into our yard. But it wasn''t until I stumbled upon an old, leather-bound book hidden within the attic that my life took a dramatic turn.

The book belonged to a mysterious figure known only as "The Clockmaker." It was an ancient tome filled with cryptic instructions on how to build time-traveling machines using nothing but gears, springs, and rusty old clock parts.

With newfound determination, I set out to build the machine, pouring all my energy into creating something that would defy the laws of physics. And then, just as I finished the final assembly, a brilliant flash of light filled the room, and everything went black.', 14);
INSERT INTO public.book VALUES ('Fictional Dreams', 'Ethan Hall', 'Fiction', 2008, NULL, 'In a world where clouds were alive, a peculiar fellow named Zephyr lived in a mansion made of fog. One day, while sipping tea from a teapot shaped like a purple eggplant, Zephyr received an unexpected visit from a talking toaster named Boris.

Boris revealed that he had been trained by the infamous Toaster Illuminati to retrieve the legendary Golden Scone, a culinary treasure hidden within the swirling vortex of the Mystic Mushroom Forest. The scone possessed the power to grant any dessert an unparalleled level of deliciousness.

As Zephyr and Boris embarked on their perilous quest, they stumbled upon a mysterious portal that led them to a planet made entirely of cream puffs. There, they encountered the enigmatic Cream Puff King, who demanded that they solve his favorite riddle: "What lies at the center of a chocolate chip cookie?" The fate of the Golden Scone hung in the balance as Zephyr and Boris navigated this surreal landscape, determined to unlock its secrets and claim the coveted dessert. Little did they know, their journey was only just beginning...', 15);
INSERT INTO public.book VALUES ('The Fantasy World', 'Ava Allen', 'Fantasy', 2019, NULL, 'In the land of forgotten socks, a lone pineapple sat atop a hill, surrounded by an aura of glittering disco balls. The pineapple, named Piney, possessed the ability to communicate with houseplants. One day, a mysterious letter arrived at Piney''s doorstep, inviting her to participate in the annual Cheese Festival.

As Piney and her entourage of dancing succulents set off for the festival, they encountered a talking eggplant who claimed to be an expert on quantum physics. The eggplant revealed that the cheese festival was actually a front for a secret society of sentient kitchen utensils, who sought to overthrow the tyrannical ruler of the land: a giant, talking toaster named Zorvath.

Piney and her plant friends joined forces with the eggplant and a motley crew of spoon-wielding rebels. Together, they battled Zorvath''s army of toast-loving minions in an epic showdown that left only one question on everyone''s mind: what happened to the lost socks? The fate of the land remained a mystery, but one thing was certain – Piney and her friends had discovered their own hidden potential, and nothing would ever be the same again.', 16);
INSERT INTO public.book VALUES ('Science and Reality', 'James Young', 'Non-Fiction', 2014, NULL, 'The Great Cheese Heist of 1957 was a scandal that shook the very foundations of Paris. It began on a typical Wednesday morning when the curator of the Louvre, Monsieur LeFleur, discovered that a prized wheel of Époisses cheese had vanished from its display case.

At first, suspicion fell upon the museum''s newest employee, a quiet and unassuming young woman named Colette. But as investigators dug deeper, they uncovered a web of deceit that led them to the museum''s own director, Monsieur Dupont.

As it turned out, Monsieur Dupont had been secretly working with a group of rogue cheese enthusiasts who had been stealing rare cheeses from museums across Europe for years. The Époisses was just the latest in a string of high-profile heists.

But what made this case even more bizarre was that the thieves had left behind a series of cryptic clues, including a note written in invisible ink and a miniature replica of the Eiffel Tower made from cheese rinds. It seemed that the masterminds behind the Great Cheese Heist were not just common thieves, but rather artists who saw the world in a different light.', 17);
INSERT INTO public.book VALUES ('Historical Tales', 'Charlotte King', 'Historical', 1975, NULL, 'In 1950s New Orleans, a mysterious antique shop appeared overnight on Bourbon Street. The sign above the door read "Curios and Wonders" in cursive letters that shimmered like moonlight. No one knew how it got there or who ran it, but rumors spread quickly about its enigmatic owner.

One stormy night, Emily, a young jazz singer, stumbled upon the shop while seeking refuge from the torrential rain. As she pushed open the door, a bell above it rang out, and the air inside was heavy with incense and forgotten memories.

Inside, shelves upon shelves of peculiar objects seemed to whisper secrets to each other. Emily spotted an ancient locket adorned with symbols that glowed like lanterns in the dark. The shop owner handed her a velvet cloak with embroidered snakes coiled around its hem.

As Emily wrapped the cloak around her shoulders, she discovered a pocket containing a key with no visible lock. Suddenly, the shop dissolved into a swirling vortex of colors and sounds, transporting her to a medieval jousting tournament. Knights clanged steel on steel as the crowd roared. Confused but exhilarated, Emily leapt onto a steed and charged forward, unaware that she was about to become the legendary Lady Aria, eternal champion of an ancient realm hidden within the swirling chaos of time itself.', 18);
INSERT INTO public.book VALUES ('Romance in Paris', 'Benjamin Wright', 'Romance', 2016, NULL, 'In a world where time was currency, the rich lived forever and the poor were left with nothing but the ticking of their own mortality clocks. Amidst this bleak landscape, a young man named Kael spent his days collecting discarded clockwork machinery in the city''s junkyards.

One day, while rummaging through a particularly pungent dumpster, Kael stumbled upon a mysterious, antique music box. As he wound it up and let its melody fill the air, a peculiar energy emanated from the box, drawing to him a beautiful, otherworldly being with skin like polished obsidian.

She introduced herself as Luna, a celestial body displaced from her orbit by an ancient cataclysm. Entranced by the music box''s haunting tune, Kael found himself falling for Luna''s ethereal charm.

As they strolled through the city''s crumbling streets, their footsteps synchronized to the rhythm of the music box. Together, they discovered that the melody held the key to manipulating time itself – slowing it down or speeding it up at will.

Hand in hand, Kael and Luna danced with the very fabric of existence, their love transcending mortal bounds as they chased the infinite possibilities hidden within the music box''s enchanting refrain.', 19);
INSERT INTO public.book VALUES ('Mystery of the Lost City', 'Ella Scott', 'Mystery', 2006, NULL, 'As I walked through the abandoned amusement park, the creaking of the rickety rollercoaster echoed through my mind. Suddenly, a gust of wind swept through, carrying with it a small, intricately carved wooden box. I picked it up, and as I did, the box began to glow.

The lights in the park flickered, and I felt myself being pulled towards a specific ride - the "Tilt-A-Whirl". I climbed into the seat, and just as the ride started, I was transported to a world made entirely of cotton candy. A figure emerged from the sugar-coated landscape: my doppelganger.

The twin revealed that it had been sent back in time to alter a crucial event - a birthday party for a giant purple eggplant named Bobo. It turned out that if Bobo hadn''t eaten the wrong flavor of cake, he would have grown into a gargantuan talking pineapple.

My doppelganger handed me a lollipop and told me I had 30 seconds to prevent this catastrophe from happening. I took a deep breath, popped the lollipop into my mouth, and spoke the ancient incantation: "Sprinkle sauce."', 20);
INSERT INTO public.book VALUES ('Biography of a Genius', 'Henry Adams', 'Biography', 1998, NULL, 'In a world where time was currency, a young woman named Zara lived a life of monotony. She worked as a temporal accountant, tasked with managing the intricate web of hours, days, and years that flowed through the city like a river.

One day, while balancing her ledgers, Zara received an unexpected visit from a mysterious figure known only as "The Croissant." He offered to trade her a single, golden pastry for all her accumulated time. Intrigued, Zara agreed, and soon found herself whisked away to a realm where the very fabric of reality was woven from sugar and spice.

There, she encountered an army of tiny, tutu-clad warriors armed with nothing but gleaming silver spoons. They were on a quest to vanquish the Dark Lord of Boredom, a monstrosity rumored to be born from the collective apathy of humanity''s most mundane office workers.

As Zara joined forces with the spoon-wielding warriors, she discovered her own hidden talent for temporal juggling – and realized that the true key to defeating the Dark Lord lay not in spoons, but in the art of perfectly folding a napkin.', 21);
INSERT INTO public.book VALUES ('Fantasy Adventures', 'Jack Turner', 'Fantasy', 2021, NULL, 'In the land of forgotten socks, a lone pineapple named Steve lived in a world where pineapples were the dominant species. One day, Steve discovered he had the ability to communicate with cats. He met a wise feline named Mr. Whiskers who possessed the power to control time.

Mr. Whiskers told Steve that the only way to defeat the evil sock monster was to gather three ancient artifacts: a rubber chicken, a can of spray paint, and a vinyl record of the 1980s hit song "Kung Fu Fighting". Steve embarked on a quest to find these artifacts, facing numerous challenges along the way.

As he navigated through the land, Steve encountered a talking tree who revealed that he was actually a time-traveling pineapple from ancient Egypt. The tree provided Steve with a magical map that led him to the rubber chicken, which was hidden inside a cheese wheel.

With the rubber chicken in hand, Steve continued his journey, using the spray paint to create a portal to another dimension. He discovered the vinyl record of "Kung Fu Fighting" was actually a key to unlock the secret of the pineapple''s forgotten past.', 23);
INSERT INTO public.book VALUES ('Fictional Reality', 'Grace Baker', 'Fiction', 2011, NULL, 'As I walked through the forest, I stumbled upon a talking tree with three eyes that changed colors depending on my mood. It was wearing a tutu and a top hat, which seemed completely out of place in the midst of nature. The tree told me it was an ancient being from a world where trees could talk and dance.

Suddenly, a portal appeared before us, leading to a land made entirely of cheese. I couldn''t believe my eyes - what kind of world would be made of cheese? The tree explained that this was the realm of Fromagea, where the inhabitants were skilled in the art of cheese-making.

As we walked through the land, we came across creatures made entirely of melted mozzarella and cheddar. They greeted us with a chorus of "Gouda day!" and invited us to join their cheese-tasting party. The tree began to dance the waltz on top of a giant wheel of brie, while I joined in with my newfound friends.

Just as we were having the time of our lives, a group of ninja pandas appeared out of nowhere, wielding tiny sushi knives and chanting "Sushi forever!" It was clear that this world was not without its conflicts. But for now, I just wanted to dance and eat all the cheese I could handle.', 22);
INSERT INTO public.book VALUES ('Science and Imagination', 'Lily Carter', 'Science Fiction', 2013, NULL, 'As I floated through the void, a giant purple eggplant hovered beside me, playing a tinny rendition of "The Blue Danube Waltz" on its built-in kazoo. The stars aligned in a peculiar pattern above us, spelling out the words "Pizza Party" in glittering cursive.

Suddenly, a chorus line of robotic flamingos emerged from the eggplant''s core, performing a choreographed dance routine to an unheard rhythm. Their legs clicked in perfect synchrony as they twirled and leaped through the cosmos.

I gazed at the spectacle, utterly perplexed, when a miniature black hole materialized beside me and began to devour my shoelaces. The flamingos halted mid-performance, their mechanical eyes fixed on the void''s growing maw.

In an unexpected twist, the eggplant unfolded itself like a giant accordion, releasing a cascade of tiny, iridescent dragons that swooped around us in dizzying arcs. The dragons left trails of glitter behind them, enveloping me in a kaleidoscope of colors and sounds.

The stars aligned once more, this time spelling out "TADA!" in bold, neon letters. And with that, the universe reset itself to a new configuration, rebooting my reality with the whimsical image of an eggplant playing kazoos amidst a swirling vortex of dragons and black holes.', 24);
INSERT INTO public.book VALUES ('Mystery of the Deep', 'Matthew Roberts', 'Mystery', 2004, NULL, 'In a small village nestled in the heart of a dense forest, there lived a mysterious woman named Echo. She was known for her ability to communicate with animals, but what the villagers didn''t know was that she was also a master of time travel.

One day, while wandering through the woods, Echo stumbled upon an ancient clockwork device buried beneath the roots of an old tree. As she touched it, she felt an electric jolt course through her veins and suddenly found herself transported to a parallel universe.

There, she encountered a talking rabbit named Zephyr who claimed to be an interdimensional guide. Together, they embarked on a quest to retrieve a lost treasure hidden within the heart of a mystical forest.

As they journeyed deeper into the woods, Echo realized that her memories were beginning to blur with those of a past life. She began to question her own identity and whether she was truly Echo or merely a pawn in some larger game.

Suddenly, Zephyr vanished, leaving Echo alone and confused. The clockwork device lay at her feet, its gears ticking away like a countdown to something unknown.', 27);
INSERT INTO public.book VALUES ('Romantic Journeys', 'Hannah Perez', 'Romance', 2015, NULL, 'As I wandered through the vast expanse of forgotten socks, I stumbled upon a peculiar portal that seemed to appear out of nowhere. Without hesitation, I stepped through its shimmering veil, and suddenly found myself in a world made entirely of cheese.

The air was filled with the sweet scent of gouda, and the ground beneath my feet was a soft layer of muenster. I wandered aimlessly, marveling at the towering wheels of brie that stretched towards the sky like giants.

As I turned a corner, I came face to face with a handsome stranger who introduced himself as Pierre, the Prince of Pecorino Romano. His piercing blue eyes locked onto mine, and I felt an inexplicable jolt of electricity run through my veins.

Without warning, Pierre began to recite a sonnet of love, his words weaving a spell that transported me to a world of pure bliss. As we stood there, the cheese around us began to melt, forming a sea of creamy white that stretched out before us like an endless ocean.

In this surreal landscape, I knew in that instant that I had found my soulmate – Pierre, the love of my life, forged from the very essence of cheese itself.', 26);
INSERT INTO public.book VALUES ('Biography of a Hero', 'Chloe Ramirez', 'Biography', 1997, NULL, 'As the clock struck midnight, a lone figure emerged from the shadows. It was a woman with piercing green eyes and jet-black hair, dressed in a long coat that billowed behind her like a dark cloud.

She walked through the deserted streets of Paris, her footsteps echoing off the walls as she made her way to the Eiffel Tower. At the top, she found a mysterious box with an intricate lock and keyhole.

Suddenly, a figure materialized beside her - a talking pineapple wearing a top hat and monocle. "Bonjour," he said in a posh accent. "I am Piney, your long-lost great-uncle."

The woman''s eyes widened as Piney handed her the box. Inside, she found a note that read: "For the love of all things fluffy, open me." With a flourish, she opened the box to reveal a giant stuffed unicorn.

As they gazed in wonder at the unicorn, a team of ninjas burst onto the scene, armed with rubber chickens and disco balls. The woman''s eyes locked onto Piney, who winked and said, "It''s time for our secret dance routine." Together, they twirled and spun, surrounded by the ninjas and their bizarre arsenal.

When the music stopped, the woman turned to Piney and asked, "But what''s your story?" Piney grinned mischievously and replied, "That''s a tale for another time, ma chère..."', 28);
INSERT INTO public.book VALUES ('Fictional Worlds', 'Ryan Thompson', 'Fiction', 2009, NULL, 'In a world where time was currency, the rich lived forever and the poor were left with nothing but the tick-tock of their own mortality. The city was a labyrinth of clockwork towers that pierced the sky like skeletal fingers.

Ava, a young woman with skin as pale as moonlight, possessed a unique gift – she could hear the whispers of the clocks. They told her secrets, begged for mercy, and whispered lies in her ear. One day, she stumbled upon a mysterious key hidden within the gears of a clock tower. The key unlocked a door that led to a realm where time was currency, and Ava discovered she was the last heir to the throne.

As she grasped the crown, the clocks began to whisper secrets in unison: "You''re not who you think you are." Ava''s world shattered like a broken clockwork mechanism. She looked down to find her hands had transformed into gears, and her feet were no longer human. The city trembled as the clocks revealed their final secret: Ava was never meant to be alive; she was just a puppet created from clockwork dreams.

Ava''s eyes turned to dust, and with them, her memories vanished like forgotten melodies in the wind. The city returned to its eternal silence, leaving behind only the echoes of broken time.', 29);


--
-- Data for Name: review; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.review VALUES (12, 'A masterpiece of storytelling.', 5, 1, 1);
INSERT INTO public.review VALUES (13, 'A masterpiece that I will reread.', 5, 2, 1);
INSERT INTO public.review VALUES (12, 'A masterpiece that I will reread.', 5, 3, 2);
INSERT INTO public.review VALUES (15, 'Great for fans of the genre.', 4, 4, 2);
INSERT INTO public.review VALUES (14, 'A captivating story with a strong message.', 4, 5, 2);
INSERT INTO public.review VALUES (7, 'Not as good as the author''s previous work.', 3, 6, 2);
INSERT INTO public.review VALUES (14, 'The plot was a bit convoluted.', 2, 7, 3);
INSERT INTO public.review VALUES (18, 'A delightful read with charming characters.', 4, 8, 3);
INSERT INTO public.review VALUES (8, 'A thought-provoking and insightful book.', 5, 10, 3);
INSERT INTO public.review VALUES (4, 'The characters felt very real.', 4, 9, 3);
INSERT INTO public.review VALUES (15, 'Amazing story and engaging characters!', 5, 11, 4);
INSERT INTO public.review VALUES (20, 'The ending was a bit rushed.', 3, 12, 4);
INSERT INTO public.review VALUES (9, 'The pacing was a bit uneven.', 3, 13, 4);
INSERT INTO public.review VALUES (4, 'The story dragged in the middle.', 2, 14, 5);
INSERT INTO public.review VALUES (17, 'A powerful story with a strong impact.', 5, 15, 5);
INSERT INTO public.review VALUES (8, 'An absolute page-turner!', 5, 16, 5);
INSERT INTO public.review VALUES (14, 'I couldn''t put it down!', 5, 17, 6);
INSERT INTO public.review VALUES (18, 'A thrilling ride from start to finish.', 5, 18, 6);
INSERT INTO public.review VALUES (4, 'Not my cup of tea, but well-written.', 2, 19, 6);
INSERT INTO public.review VALUES (19, 'The pacing was a bit uneven.', 3, 20, 7);
INSERT INTO public.review VALUES (2, 'Amazing story and engaging characters!', 5, 21, 7);
INSERT INTO public.review VALUES (18, 'The narrative was a bit disjointed.', 2, 22, 7);
INSERT INTO public.review VALUES (1, 'Beautifully written and engaging.', 5, 23, 7);
INSERT INTO public.review VALUES (13, 'A bit too long for my taste.', 3, 24, 8);
INSERT INTO public.review VALUES (3, 'An absolute page-turner!', 5, 25, 8);
INSERT INTO public.review VALUES (1, 'A fascinating exploration of themes.', 4, 26, 8);
INSERT INTO public.review VALUES (7, 'A delightful and charming tale.', 4, 27, 9);
INSERT INTO public.review VALUES (18, 'An absolute page-turner!', 5, 28, 9);
INSERT INTO public.review VALUES (12, 'Amazing story and engaging characters!', 5, 29, 9);
INSERT INTO public.review VALUES (11, 'The narrative was a bit disjointed.', 2, 30, 9);
INSERT INTO public.review VALUES (5, 'The writing style wasn''t for me.', 2, 31, 9);
INSERT INTO public.review VALUES (8, 'The plot twists were a bit obvious.', 3, 32, 10);
INSERT INTO public.review VALUES (6, 'Good pace but could improve the ending.', 4, 33, 10);
INSERT INTO public.review VALUES (14, 'The story dragged in the middle.', 2, 34, 10);
INSERT INTO public.review VALUES (17, 'A delightful and charming tale.', 4, 35, 10);
INSERT INTO public.review VALUES (12, 'A compelling read with strong characters.', 4, 36, 10);
INSERT INTO public.review VALUES (17, 'A bit too predictable for my liking.', 3, 37, 11);
INSERT INTO public.review VALUES (1, 'An absolute page-turner!', 5, 38, 11);
INSERT INTO public.review VALUES (16, 'An epic story that stays with you.', 5, 39, 11);
INSERT INTO public.review VALUES (17, 'A delightful and charming tale.', 4, 40, 12);
INSERT INTO public.review VALUES (18, 'The dialogue felt a bit forced.', 2, 41, 13);
INSERT INTO public.review VALUES (12, 'A bit too predictable for my liking.', 3, 42, 14);
INSERT INTO public.review VALUES (4, 'A unique take on a classic theme.', 5, 43, 14);
INSERT INTO public.review VALUES (14, 'A well-paced and engaging story.', 4, 44, 14);
INSERT INTO public.review VALUES (7, 'The plot was a bit thin.', 3, 45, 14);
INSERT INTO public.review VALUES (5, 'The dialogue felt a bit forced.', 2, 46, 14);
INSERT INTO public.review VALUES (14, 'A masterpiece of storytelling.', 5, 47, 15);
INSERT INTO public.review VALUES (5, 'The characters lacked depth.', 2, 48, 15);
INSERT INTO public.review VALUES (2, 'Not as good as the author''s previous work.', 3, 49, 15);
INSERT INTO public.review VALUES (11, 'Amazing story and engaging characters!', 5, 50, 16);
INSERT INTO public.review VALUES (8, 'An absolute page-turner!', 5, 51, 16);
INSERT INTO public.review VALUES (13, 'The ending was a bit unsatisfying.', 3, 52, 16);
INSERT INTO public.review VALUES (9, 'Good pace but could improve the ending.', 4, 53, 16);
INSERT INTO public.review VALUES (10, 'Intriguing mystery with clever twists.', 4, 54, 17);
INSERT INTO public.review VALUES (7, 'A delightful read with charming characters.', 4, 55, 17);
INSERT INTO public.review VALUES (19, 'A solid read with a few surprises.', 4, 56, 18);
INSERT INTO public.review VALUES (11, 'The plot was a bit convoluted.', 2, 57, 18);
INSERT INTO public.review VALUES (6, 'I couldn''t put it down!', 5, 58, 18);
INSERT INTO public.review VALUES (13, 'A bit predictable but still fun.', 3, 59, 18);
INSERT INTO public.review VALUES (12, 'An epic story that stays with you.', 5, 60, 18);
INSERT INTO public.review VALUES (20, 'Intriguing mystery with clever twists.', 4, 61, 19);
INSERT INTO public.review VALUES (19, 'The writing style wasn''t for me.', 2, 62, 19);
INSERT INTO public.review VALUES (12, 'A powerful story with a strong impact.', 5, 64, 20);
INSERT INTO public.review VALUES (18, 'Amazing story and engaging characters!', 5, 65, 20);
INSERT INTO public.review VALUES (2, 'Great for fans of the genre.', 4, 63, 20);
INSERT INTO public.review VALUES (15, 'A gripping tale with unexpected twists.', 5, 66, 21);
INSERT INTO public.review VALUES (7, 'The plot twists were a bit obvious.', 3, 67, 21);
INSERT INTO public.review VALUES (17, 'A delightful read with charming characters.', 4, 68, 21);
INSERT INTO public.review VALUES (17, 'The ending was a bit unsatisfying.', 3, 69, 22);
INSERT INTO public.review VALUES (1, 'A bit slow at the start but picks up well.', 3, 70, 22);
INSERT INTO public.review VALUES (3, 'A unique take on a classic theme.', 5, 71, 23);
INSERT INTO public.review VALUES (2, 'Not as good as the author''s previous work.', 3, 72, 24);
INSERT INTO public.review VALUES (11, 'A delightful and charming tale.', 4, 73, 24);
INSERT INTO public.review VALUES (14, 'A masterpiece that I will reread.', 5, 74, 24);
INSERT INTO public.review VALUES (6, 'A solid read with a few surprises.', 4, 75, 24);
INSERT INTO public.review VALUES (12, 'The plot was a bit thin.', 3, 76, 24);
INSERT INTO public.review VALUES (14, 'Predictable but enjoyable.', 3, 77, 25);
INSERT INTO public.review VALUES (16, 'A bit predictable but still fun.', 3, 78, 25);
INSERT INTO public.review VALUES (18, 'Could use more depth in the plot.', 3, 79, 25);
INSERT INTO public.review VALUES (10, 'A heartwarming story with depth.', 5, 80, 25);
INSERT INTO public.review VALUES (4, 'An absolute page-turner!', 5, 81, 26);
INSERT INTO public.review VALUES (20, 'Great for fans of the genre.', 4, 83, 26);
INSERT INTO public.review VALUES (7, 'Predictable but enjoyable.', 3, 84, 26);
INSERT INTO public.review VALUES (10, 'The ending was a bit unsatisfying.', 3, 82, 26);
INSERT INTO public.review VALUES (5, 'A captivating story with a strong message.', 4, 85, 27);
INSERT INTO public.review VALUES (7, 'A truly inspiring and uplifting read.', 5, 86, 27);
INSERT INTO public.review VALUES (18, 'An unforgettable journey.', 5, 87, 28);
INSERT INTO public.review VALUES (7, 'Could use more depth in the plot.', 3, 88, 28);
INSERT INTO public.review VALUES (10, 'Not my cup of tea, but well-written.', 2, 89, 28);
INSERT INTO public.review VALUES (2, 'Not my cup of tea, but well-written.', 2, 90, 29);
INSERT INTO public.review VALUES (6, 'The ending was a bit rushed.', 3, 91, 29);
INSERT INTO public.review VALUES (16, 'Intriguing mystery with clever twists.', 4, 92, 29);


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public."user" VALUES ('books_admin', 1, true, 'books_admin::token');


--
-- Name: book_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.book_id_seq', 29, true);


--
-- Name: review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.review_id_seq', 92, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 2, true);


--
-- Name: book book_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book
    ADD CONSTRAINT book_pkey PRIMARY KEY (id);


--
-- Name: review review_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.review
    ADD CONSTRAINT review_pkey PRIMARY KEY (id);


--
-- Name: book uq_title_author; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book
    ADD CONSTRAINT uq_title_author UNIQUE (title, author);


--
-- Name: user uq_username; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT uq_username UNIQUE (username);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: review review_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.review
    ADD CONSTRAINT review_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.book(id);


--
-- PostgreSQL database dump complete
--

