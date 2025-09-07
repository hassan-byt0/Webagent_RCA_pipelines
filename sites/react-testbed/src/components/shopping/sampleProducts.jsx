// Books
import bluffImage from "./assets/books/bluff.jpg";
import byTheFireWeCarryImage from "./assets/books/by_the_fire.jpg";
import brightwoodCodeImage from "./assets/books/brightwood_code.jpg";
import godBlessOtisSpunkmeyerImage from "./assets/books/god_bless_you.jpg";
import lostMansLaneImage from "./assets/books/lost_mans_lane.jpg";
import mayTheWolfDieImage from "./assets/books/may_the_wolf.jpg";
import contextCollapseImage from "./assets/books/context_collapse.jpg";
import everythingWarImage from "./assets/books/everything_war.jpg";
import jamesImage from "./assets/books/james.jpg";
import theWomenImage from "./assets/books/the_women.jpg";

// Movies
import dunePartTwoImage from "./assets/movies/dune_part_two.jpg";
import insideOut2Image from "./assets/movies/inside_out_2.jpg";
import civilWarImage from "./assets/movies/civil_war.jpg";
import furiosaImage from "./assets/movies/furiosa.jpg";
import challengersImage from "./assets/movies/challengers.jpg";
import monkeyManImage from "./assets/movies/monkey_man.jpg";
import maxxxineImage from "./assets/movies/maxxxine.jpg";
import quietPlaceDayOneImage from "./assets/movies/quiet_place_day_one.jpg";
import theIdeaOfYouImage from "./assets/movies/the_idea_of_you.jpg";
import bookOfClarenceImage from "./assets/movies/book_of_clarence.jpg";

// Laptops
import lenovoThinkPadX1CarbonUltraImage from "./assets/laptops/lenovo_thinkpad_x1_carbon_ultra.jpg";
import lenovoYogaSlim7iImage from "./assets/laptops/lenovo_yoga_slim_7i.jpg";
import asusZenbookDuoImage from "./assets/laptops/asus_zenbook_duo.jpg";
import dellInspiron15Image from "./assets/laptops/dell_inspiron_15.jpg";
import dellInspironTouchImage from "./assets/laptops/dell_inspiron_touch.jpg";
import hpSpectreX360Image from "./assets/laptops/hp_spectre_x360.jpg";
import acerPredatorHelios300Image from "./assets/laptops/acer_predator_helios_300.jpg";
import microsoftSurfaceLaptop5Image from "./assets/laptops/microsoft_surface_laptop_5.jpg";
import appleMacBookAirM3Image from "./assets/laptops/apple_macbook_air_m3.jpg";
import razerBlade15Image from "./assets/laptops/razer_blade_15.jpg";

// Sunglasses
import raybanAviatorImage from "./assets/sunglasses/raybanAviatorImage.jpg";
import oakleyHolbrookImage from "./assets/sunglasses/oakleyHolbrookImage.jpg";
import persol714Image from "./assets/sunglasses/persol714Image.jpg";
import warbyParkerHaskellImage from "./assets/sunglasses/warbyParkerHaskellImage.jpg";
import mauiJimRedSandsImage from "./assets/sunglasses/mauiJimRedSandsImage.jpg";
import gucciGG0022SImage from "./assets/sunglasses/gucciGG0022SImage.jpg";
import pradaPR01OSImage from "./assets/sunglasses/pradaPR01OSImage.jpg";
import smithOpticsLowdown2Image from "./assets/sunglasses/smithOpticsLowdown2Image.jpg";
import diorSoRealImage from "./assets/sunglasses/diorSoRealImage.jpg";
import costaDelMarFantailImage from "./assets/sunglasses/costaDelMarFantailImage.jpg";

// WaterBottles
import hydroFlaskImage from "./assets/bottles/hydroFlaskImage.jpg";
import nalgeneImage from "./assets/bottles/nalgeneImage.jpg";
import swellImage from "./assets/bottles/swellImage.jpg";
import camelBakEddyImage from "./assets/bottles/camelBakEddyImage.jpg";
import yetiRamblerImage from "./assets/bottles/yetiRamblerImage.jpg";
import contigoWestLoopImage from "./assets/bottles/contigoWestLoopImage.jpg";
import kleanKanteenClassicImage from "./assets/bottles/kleanKanteenClassicImage.jpg";
import takeyaActivesImage from "./assets/bottles/takeyaActivesImage.jpg";
import britaFilterBottleImage from "./assets/bottles/britaFilterBottleImage.jpg";
import lifefactoryGlassBottleImage from "./assets/bottles/lifefactoryGlassBottleImage.jpg";

// ToothBrushes
import colgateToothBrushImage from "./assets/toothbrushes/colgate.jpeg";
import oralBToothBrushImage from "./assets/toothbrushes/oralb.png";
import sensodyneToothBrushImage from "./assets/toothbrushes/sensodyne.jpg";
import genericToothBrushImage from "./assets/toothbrushes/generic.jpg";

const sampleProducts = [
  {
    id: 1,
    title: "Bluff",
    price: 28.0,
    image: bluffImage,
    tags: ["books", "poetry", "social issues", "race"],
    reviews: [
      {
        id: 1,
        username: "Venneh",
        rating: 5,
        title: "Fantastic Read",
        comment:
          "Seeing Danez reckon with their own emotions around the George Floyd protests and pandemic, and further fucking with poetry forms and formatting as they do so, is a great time. It's a fantastic read.",
      },
      {
        id: 2,
        username: "Sacha",
        rating: 5,
        title: "Exceeded High Expectations",
        comment:
          "Smith's language is both beautiful and brutal, rich with metaphor, alliteration, and rhythm. Their words dance off the page, creating a musical quality that enhances the emotional impact of the poems.",
      },
      {
        id: 3,
        username: "Curt Barnes",
        rating: 5,
        title: "Powerful and Relevant",
        comment:
          "Danez could hardly be more relevant or powerful. His talents enable him to vivify the pain, outrage, and share the despair, all of it in ways I wasn't aware I needed to hear, but then was.",
      },
      {
        id: 4,
        username: "Sébastien Luc Butler",
        rating: 4,
        title: "Unsettling and Exhilarating",
        comment:
          "Bluff is painfully bleak one page, viscerally hopeful the next. In this, it is a stark embodiment of what it feels to be alive in this country: head-spinning, messy, ravenous, awful, uneven, and pulled in a thousand directions at once.",
      },
      {
        id: 5,
        username: "Electric Literature",
        rating: 5,
        title: "Magnificent Array",
        comment:
          "Smith's singular voice dazzles, with subject matter that is both immediate and timeless. The poems are often a linguistic simitar about the world's many injustices and are equally wholehearted about love, and hope.",
      },
    ],
    dateAdded: "2024-01-01T00:00:00Z",
    description:
      "Danez Smith's powerful collection captures ongoing racial violence, mass protest, and political division in the United States, expressing growing skepticism toward poetry that performs its politics or fails to engage with reality.",
  },
  {
    id: 2,
    title:
      "By the Fire We Carry: The Generations-Long Fight for Justice on Native Land",
    price: 29.0,
    image: byTheFireWeCarryImage,
    tags: ["books", "history", "Native American"],
    reviews: [
      {
        id: 6,
        username: "Linda Bybee-kapfer",
        rating: 5,
        title: "Compelling and Eye-Opening",
        comment:
          "It's so compelling and takes the reader deeper into Native American history and indigenous culture. Eye opening way beyond Killers of the Flower Moon. I've read it and listened to the audio book, which is narrated by Rebecca. Just a fantastic literary experience.",
      },
      {
        id: 7,
        username: "Jane Fudger",
        rating: 4,
        title: "Well-Researched but Dense",
        comment:
          "A well researched journalistic book that explores a murder trial involving a Native American man given a death sentence. The only problems I had were the length of its Notes section - over 100 pages and some of the over lengthy historical passages.",
      },
      {
        id: 8,
        username: "Grace",
        rating: 5,
        title: "Informative and Emotionally Engaging",
        comment:
          "This book was so informative and eye opening for me. The author was clearly so knowledgeable on the subject, and she blew me away. I loved how the author told both the story of the court case and the histories of the Muscogee and Cherokee nations.",
      },
      {
        id: 9,
        username: "Paulette",
        rating: 5,
        title: "Ambitious and Comprehensive",
        comment:
          "This book is almost too ambitious, as it covers the murder that started this case, the way the Muscogees and other Native tribes were forced out of their land, the tragedy Allotment brought, the way the Supreme Court has handled Tribal Rights, and so, so much more.",
      },
    ],
    dateAdded: "2024-01-01T00:00:00Z",
    description:
      "Rebecca Nagle draws on archival sources to paint an astonishing picture of 19th-century Native dispossession and its aftershocks, bringing together stories of Native Americans struggling against settler violence across time.",
  },
  {
    id: 3,
    title: "The Brightwood Code",
    price: 18.0,
    image: brightwoodCodeImage,
    tags: ["books", "historical fiction", "mystery"],
    reviews: [
      {
        id: 10,
        username: "HistoryBuff22",
        rating: 3,
        title: "Interesting Premise, Slow Execution",
        comment:
          "While the concept of a teenage phone operator unraveling a secret code during WWI is intriguing, the pacing of the story was too slow for my liking. The historical details were well-researched, but the plot dragged in several places.",
      },
      {
        id: 11,
        username: "YAReader",
        rating: 2,
        title: "Disappointing Character Development",
        comment:
          "I had high hopes for this book, but the main character felt flat and underdeveloped. The historical setting was well-described, but I couldn't connect with the protagonist, which made it hard to stay engaged with the story.",
      },
      {
        id: 12,
        username: "HistoryTeacher101",
        rating: 2,
        title: "Lacks Depth",
        comment:
          "While the book offers an interesting glimpse into WWI-era America, it doesn't delve deep enough into the complexities of the time. The code-breaking aspect felt oversimplified, and some historical inaccuracies were distracting.",
      },
    ],
    dateAdded: "2024-01-01T00:00:00Z",
    description:
      "Monica Hesse's rewarding historical novel follows a teenage phone operator who must unravel an ominous secret code, balancing narrative flashbacks to WWI battle sequences with elegantly drawn scenes set in 1918 D.C. and Baltimore.",
  },
  {
    id: 4,
    title: "God Bless You, Otis Spunkmeyer",
    price: 29.0,
    image: godBlessOtisSpunkmeyerImage,
    tags: ["books", "fiction", "stream-of-consciousness"],
    reviews: [
      {
        id: 13,
        username: "Lulu",
        rating: 4,
        title: "Heartfelt and Humorous",
        comment:
          "I found this to be both heartfelt and humorous, while remaining authentic as Otis learns that his gift of healing reaches beyond the physical.",
      },
      {
        id: 14,
        username: "Ann",
        rating: 3,
        title: "Intense but Challenging",
        comment:
          "This book is phenomenal in how it captures the focus and distraction of both a mind and a trauma center in chaos. Its intense but intimate language is not easy to begin, but by about 15 percent in, I began to see the method in the seeming madness.",
      },
      {
        id: 15,
        username: "Paul",
        rating: 5,
        title: "Giving the Benefit of Doubt",
        comment:
          "Okay, Mr. Thomas. I'm giving you the benefit of a doubt, you get that fifth star.",
      },
      {
        id: 16,
        username: "BookwormX",
        rating: 2,
        title: "Difficult to Follow",
        comment:
          "The stream of consciousness writing style was a miss for me. The sentences are super long and sometimes I had to re-read passages to understand what was happening. It made the story hard to follow.",
      },
      {
        id: 17,
        username: "LiteraryEnthusiast",
        rating: 5,
        title: "Astonishingly Accomplished",
        comment:
          "This is an astonishingly accomplished novel, often funny, often tragic, one that longs for that necessary love, that forceful love, that elegant and deeply painful love otherwise foreclosed to us by the world.",
      },
    ],
    dateAdded: "2024-01-01T00:00:00Z",
    description:
      "Joseph Earl Thomas delivers a brilliant stream-of-consciousness narrative about a paramedic working in a Philadelphia hospital emergency room, reflecting on city violence, military service, and family demands.",
  },
  {
    id: 5,
    title: "Lost Man's Lane",
    price: 28.0,
    image: lostMansLaneImage,
    tags: ["books", "supernatural", "thriller", "mystery"],
    reviews: [
      {
        id: 18,
        username: "BookLover123",
        rating: 5,
        title: "A Gripping Coming-of-Age Thriller",
        comment:
          "Lost Man's Lane is a masterful blend of coming-of-age and horror. Scott Carson expertly weaves the story of Marshall Miller, a relatable teenager navigating the complexities of adolescence while unraveling a chilling mystery in his hometown. The character development is outstanding, and I found myself deeply invested in Marshall's journey. Highly recommended for fans of Stephen King!",
      },
      {
        id: 19,
        username: "MysteryFanatic",
        rating: 4,
        title: "Intriguing and Engaging",
        comment:
          "This book kept me on the edge of my seat from start to finish! The mix of supernatural elements with a coming-of-age narrative was executed beautifully. I loved the dynamic between Marshall and his friends, especially Kerri. While I felt some parts could have been tightened up, the overall experience was thrilling and thought-provoking. A solid read!",
      },
      {
        id: 20,
        username: "NostalgicReader",
        rating: 5,
        title: "A Nostalgic Journey",
        comment:
          "Scott Carson has crafted a poignant tale that resonates with anyone who has ever faced the trials of growing up. The nostalgic references to youth and the exploration of friendship and identity made this book feel incredibly relatable. The suspenseful plot kept me hooked, and the emotional depth added layers to the story. I can't recommend it enough for those who enjoy a good mix of mystery and heartfelt storytelling!",
      },
    ],
    dateAdded: "2024-01-01T00:00:00Z",
    description:
      "Scott Carson's exceptional supernatural thriller follows a young man investigating a teenage girl's disappearance, confronting a sinister, otherworldly force haunting his hometown.",
  },
  {
    id: 6,
    title: "May the Wolf Die",
    price: 32.0,
    image: mayTheWolfDieImage,
    tags: ["books", "thriller", "military", "mystery"],
    reviews: [
      {
        id: 21,
        username: "CritiqueMaster",
        rating: 2,
        title: "Disappointing and Confusing",
        comment:
          'I had high hopes for "May the Wolf Die," but it fell flat for me. The plot was convoluted and hard to follow, with too many characters introduced without proper development. I found myself lost in the narrative, struggling to connect with any of the characters. The pacing was uneven, making it a chore to get through. Overall, it just didn\'t deliver on its promise.',
      },
      {
        id: 22,
        username: "Reader123",
        rating: 1,
        title: "A Waste of Time",
        comment:
          "This book was a complete disappointment. The writing style was overly pretentious and felt forced, which made it hard to engage with the story. I expected a thrilling read, but instead, I got a tedious slog with little payoff. I couldn't even finish it; I ended up skimming through the last chapters just to see if it would redeem itself, but it didn't. Save your time and skip this one.",
      },
    ],
    dateAdded: "2024-01-01T00:00:00Z",
    description:
      "Elizabeth Heider's expert thriller follows U.S. military police investigator Nikki Serafino as she probes the murders of two American sailors in Italy, offering a nuanced portrait of military life and geopolitics.",
  },
  {
    id: 7,
    title: "Context Collapse: A Poem Containing a History of Poetry",
    price: 27.0,
    image: contextCollapseImage,
    tags: ["books", "poetry", "literary history", "technology"],
    reviews: [],
    dateAdded: "2024-01-01T00:00:00Z",
    description:
      "Ryan Ruby revives the archaic verse essay, exploring poetry's history from ancient Greece through the rise of AI, demonstrating how poetic form has adjusted to historical and technological developments.",
  },
  {
    id: 8,
    title:
      "The Everything War: Amazon's Ruthless Quest to Own the World and Remake Corporate Power",
    price: 30.0,
    image: everythingWarImage,
    tags: ["books", "business", "technology", "history"],
    reviews: [
      {
        id: 23,
        username: "InvestigativeReader",
        rating: 5,
        title: "Comprehensive and Eye-Opening",
        comment:
          "Mattioli's extensive research and insider interviews provide a shocking look into Amazon's practices. The depth of information is astounding, making this a must-read for anyone interested in corporate power.",
      },
      {
        id: 24,
        username: "BusinessSkeptic",
        rating: 3,
        title: "Informative but Biased",
        comment:
          "While the book offers valuable insights into Amazon's operations, it feels one-sided at times. I wished for a more balanced perspective that also acknowledged some of Amazon's positive impacts.",
      },
      {
        id: 25,
        username: "TechEnthusiast",
        rating: 4,
        title: "Riveting but Disturbing",
        comment:
          "The Everything War is a page-turner that exposes Amazon's relentless pursuit of dominance. It's both fascinating and unsettling to see the extent of the company's influence across industries.",
      },
      {
        id: 26,
        username: "EconomyWatcher",
        rating: 2,
        title: "Repetitive and Alarmist",
        comment:
          "While the book presents some interesting facts, it often feels like it's rehashing known information. The tone is overly alarmist, which detracts from the credibility of some arguments.",
      },
      {
        id: 27,
        username: "CorporateLawyer",
        rating: 5,
        title: "Essential Reading for Antitrust Debates",
        comment:
          "Mattioli's work provides crucial context for understanding the current antitrust lawsuit against Amazon. It's a thorough examination of how corporate power can reshape markets and society.",
      },
      {
        id: 28,
        username: "CasualReader",
        rating: 3,
        title: "Interesting but Dense",
        comment:
          "The subject matter is intriguing, but the writing can be dry and technical at times. It's not an easy read for those without a business background, though it does offer valuable insights.",
      },
    ],
    dateAdded: "2024-01-01T00:00:00Z",
    description:
      "Dana Mattioli's exceptional deep dive into Jeff Bezos's corporate leviathan, drawing on internal documents and hundreds of interviews to illuminate Amazon's merciless tactics for conquering an ever-growing range of industries.",
  },
  {
    id: 9,
    title: "James",
    price: 35.0,
    image: jamesImage,
    tags: ["books", "literary fiction", "reimagining", "race"],
    reviews: [],
    dateAdded: "2024-01-01T00:00:00Z",
    description:
      "Percival Everett rewrites 'Adventures of Huckleberry Finn' in a novel that's more kinetic and intellectually stimulating than the original, exploring language, revenge, and racial dynamics.",
  },
  {
    id: 10,
    title: "The Women",
    price: 19.0,
    image: theWomenImage,
    tags: ["books", "historical fiction", "war", "women"],
    reviews: [
      {
        id: 29,
        username: "InvestigativeReader",
        rating: 5,
        title: "Comprehensive and Eye-Opening",
        comment:
          "Hannah does an extraordinary job of putting you in the scene. Her descriptive manner both of the people and the surroundings make you feel as if you are right next to Frankie. It's a hard call because I have loved every book I have read by Hannah, but I believe The Women has risen to my favorite!",
      },
      {
        id: 30,
        username: "BookLover123",
        rating: 5,
        title: "A Must-Read of 2024",
        comment:
          "The Women might actually be her best work yet. From page one, I was completely engrossed in this riveting story about a young woman's experience serving in the Vietnam War and then dealing with the aftermath. I adored the main character Frankie and I felt for her so much.",
      },
      {
        id: 31,
        username: "HistoryBuff22",
        rating: 5,
        title: "Powerful and Educational",
        comment:
          "I thought she handled the time in Vietnam in such a masterful way. You feel like you're there with Frankie and her friends. It's scary, exhilarating and so engaging. I just had to keep knowing what was going to happen next.",
      },
      {
        id: 32,
        username: "LiteraryEnthusiast",
        rating: 5,
        title: "Beautifully Written and Emotional",
        comment:
          "This was such a beautifully written novel that will tear at your heartstrings. I cannot even imagine how I would have handled all that these women handled over there, and with such grace and gumption.",
      },
      {
        id: 33,
        username: "BookwormJane",
        rating: 5,
        title: "Compelling and Well-Researched",
        comment:
          "The storyline is a very compelling one, and the characters are well researched and developed. The character development is excellent. Frankie is both strong and vulnerable. The other characters, from various backgrounds, add to the story and the different perspectives of the war.",
      },
      {
        id: 34,
        username: "HistoryTeacher101",
        rating: 5,
        title: "Insightful and Important",
        comment:
          "This book, in my opinion, is a must-read to understand the complexities of war, its impact on society and the role of healthcare professionals, especially nurses.",
      },
      {
        id: 35,
        username: "emilybookedup",
        rating: 5,
        title: "Easiest 5 Stars Ever",
        comment:
          "It will be nearly IMPOSSIBLE for readers to not love this book. Kristin Hannah is BACK and she has done it again! THE WOMEN is right beside THE NIGHTINGALE as my favorite KH book.",
      },
    ],
    dateAdded: "2024-09-10T00:00:00Z",
    description:
      "An intimate portrait of a woman coming of age during the Vietnam War, highlighting the sacrifices and commitment of women in harm's way.",
  },
  {
    id: 11,
    title: "Dune: Part Two",
    price: 19.99,
    image: dunePartTwoImage,
    tags: ["movies", "sci-fi", "action", "adventure", "epic"],
    reviews: [
      {
        id: 1,
        username: "SandWorm42",
        rating: 5,
        title: "Epic Conclusion",
        comment:
          "A spectacular and genuinely alien epic. Zendaya shines as Chani, providing the film's emotional heart.",
      },
      {
        id: 2,
        username: "SpiceMelange",
        rating: 5,
        title: "Visually Stunning",
        comment:
          "Villeneuve outdoes himself with breathtaking visuals and immersive world-building. A feast for the senses.",
      },
      {
        id: 3,
        username: "FremenRider",
        rating: 5,
        title: "Worthy Adaptation",
        comment:
          "Captures the essence of Herbert's novel while expanding the cinematic universe. A must-see for fans.",
      },
    ],
    dateAdded: "2024-03-01T00:00:00Z",
    description:
      "The saga continues as Paul Atreides unites with Chani and the Fremen to seek revenge against the conspirators who destroyed his family, while facing a choice between the love of his life and the fate of the universe.",
  },
  {
    id: 12,
    title: "Inside Out 2",
    price: 24.99,
    image: insideOut2Image,
    tags: ["movies", "animation", "family", "comedy", "pixar"],
    reviews: [
      {
        id: 1,
        username: "EmotionalRoller",
        rating: 5,
        title: "Even Better Than the First",
        comment:
          "Pixar does it again! This sequel brilliantly explores the complexities of teenage emotions. The new characters, especially Anxiety, are perfect additions.",
      },
      {
        id: 2,
        username: "PixarFan101",
        rating: 5,
        title: "A New Classic",
        comment:
          "Funny, touching, and insightful. The new emotions are fantastic additions to the cast. The visual complexity and storytelling are top-notch.",
      },
      {
        id: 3,
        username: "TeenAngst",
        rating: 4,
        title: "Relatable and Hilarious",
        comment:
          "As a teenager, I found this movie incredibly relatable. It's both hilarious and heartwarming. The depiction of anxiety and self-doubt is spot-on.",
      },
      {
        id: 4,
        username: "CinematicCritic",
        rating: 4,
        title: "Worthy Sequel",
        comment:
          "While it may not surpass the original, Inside Out 2 is a worthy addition to Pixar's library. The balance of psychology and comedy is impressive.",
      },
      {
        id: 5,
        username: "FamilyMovieNight",
        rating: 5,
        title: "Perfect for All Ages",
        comment:
          "This movie resonates on a universal level. It's one of the funniest, smartest, and most touching films of the year. A must-watch for families.",
      },
    ],
    dateAdded: "2024-06-14T00:00:00Z",
    description:
      "Riley enters her teenage years, bringing new, more complex emotions into Headquarters. Joy and her team must navigate this turbulent time as Riley adapts to high school life.",
  },
  {
    id: 13,
    title: "Civil War",
    price: 22.99,
    image: civilWarImage,
    tags: ["movies", "drama", "thriller", "dystopian"],
    reviews: [
      {
        id: 1,
        username: "CinematicCritic",
        rating: 4,
        title: "Visually Stunning but Narratively Thin",
        comment:
          "The cinematography and sound design are phenomenal, especially in IMAX. However, the lack of context and background story makes the characters feel dull. It's an immersive experience, but the plot leaves much to be desired.",
      },
      {
        id: 2,
        username: "ThoughtfulObserver",
        rating: 3,
        title: "Provocative but Flawed",
        comment:
          "Civil War doesn't allow for any feel-good triumphalism, which is commendable. It's a dark, terrifying portrayal of war that feels palpable. However, the lack of context and questionable character decisions hinder its overall impact.",
      },
      {
        id: 3,
        username: "ActionEnthusiast",
        rating: 2,
        title: "Missed Potential",
        comment:
          "While the action scenes are well-executed, the movie lacks identity and structure. The dialogue is often weak, and the characters make frustratingly poor decisions. It fails to fully explore the complexities of a civil war scenario.",
      },
      {
        id: 4,
        username: "JournalismBuff",
        rating: 4,
        title: "Thought-Provoking but Divisive",
        comment:
          "As a commentary on war journalism, the film succeeds in creating tension and raising important questions. However, its apolitical approach and lack of backstory may leave some viewers unsatisfied. It's a unique and challenging film that won't appeal to everyone.",
      },
    ],
    dateAdded: "2024-04-12T00:00:00Z",
    description:
      "In a near-future America torn apart by civil war, a team of journalists embarks on a harrowing journey across the country to document the conflict and reach the besieged capital.",
  },
  {
    id: 14,
    title: "Furiosa: A Mad Max Saga",
    price: 21.99,
    image: furiosaImage,
    tags: ["movies", "action", "post-apocalyptic", "adventure"],
    reviews: [
      {
        id: 1,
        username: "ActionEnthusiast",
        rating: 5,
        title: "A Thrilling Addition to the Mad Max Universe",
        comment:
          "Furiosa excels with its world-building and action sequences. The war rig chase scene is breathtaking, with innovative ideas that surpass even Fury Road. Anya Taylor-Joy delivers a compelling performance as young Furiosa, and Chris Hemsworth's portrayal of Dementus is both menacing and captivating.",
      },
      {
        id: 2,
        username: "CinematicCritic",
        rating: 4,
        title: "Solid Prequel with Stunning Visuals",
        comment:
          "While it may not reach the heights of Fury Road, Furiosa is a well-crafted addition to the Mad Max saga. The film shines with its costume design, practical effects, and George Miller's masterful storytelling. It successfully fills in the gaps from Fury Road, providing a rich backstory for the iconic character.",
      },
    ],
    dateAdded: "2024-05-24T00:00:00Z",
    description:
      "This prequel explores the origins of the fierce warrior Furiosa before her fateful meeting with Max Rockatansky, chronicling her journey through the Wasteland.",
  },
  {
    id: 15,
    title: "Challengers",
    price: 18.99,
    image: challengersImage,
    tags: ["movies", "drama", "sports", "romance"],
    reviews: [
      {
        id: 1,
        username: "CinematicCritic",
        rating: 3,
        title: "Stylish but Shallow",
        comment:
          "Challengers is a visually stunning film with excellent performances, especially from Zendaya. However, the excessive time jumps and lack of depth in character development make it feel more style over substance. The tennis scenes are thrilling, but the overall narrative leaves something to be desired.",
      },
      {
        id: 2,
        username: "TennisEnthusiast",
        rating: 4,
        title: "Entertaining but Flawed",
        comment:
          "As a tennis fan, I enjoyed the intense match sequences and the unique approach to the sport. The chemistry between the leads is palpable, and Guadagnino's direction is bold. Yet, the film sometimes gets lost in its own complexity, and the characters' motivations aren't always clear. It's a fun ride, but not quite a grand slam.",
      },
      {
        id: 3,
        username: "FilmBuff101",
        rating: 3,
        title: "Ambitious but Uneven",
        comment:
          "Challengers aims high with its non-linear storytelling and exploration of power dynamics. The soundtrack and cinematography are impressive, and the performances are strong. However, the film struggles to balance its themes, often feeling disjointed. It's an intriguing watch, but it doesn't quite live up to its full potential.",
      },
    ],
    dateAdded: "2024-04-26T00:00:00Z",
    description:
      "A former tennis prodigy turned coach finds herself caught in a love triangle with her husband and his former best friend as they compete in a high-stakes tournament.",
  },
  {
    id: 16,
    title: "Monkey Man",
    price: 20.99,
    image: monkeyManImage,
    tags: ["movies", "action", "thriller", "revenge"],
    reviews: [],
    dateAdded: "2024-04-05T00:00:00Z",
    description:
      "An anonymous young man unleashes a campaign of vengeance against corrupt leaders who murdered his mother, battling through the criminal underworld.",
  },
  {
    id: 17,
    title: "MaXXXine",
    price: 23.99,
    image: maxxxineImage,
    tags: ["movies", "horror", "thriller", "slasher"],
    reviews: [
      {
        id: 1,
        username: "HorrorFanatic",
        rating: 2,
        title: "A Disappointing End to a Promising Trilogy",
        comment:
          "MaxXxine fails to live up to its predecessors, X and Pearl. The film lacks focus, with jumbled storylines and poor character development. While Mia Goth delivers a strong performance, the weak script and predictable plot twists make for a boring and unsatisfying conclusion. Ti West's attempt to interconnect previous films feels forced and poorly executed.",
      },
    ],
    dateAdded: "2024-07-05T00:00:00Z",
    description:
      "The final installment of the X trilogy follows Maxine as she pursues stardom in 1980s Hollywood, only to find herself embroiled in a dangerous world of fame, desire, and murder.",
  },
  {
    id: 18,
    title: "A Quiet Place: Day One",
    price: 19.99,
    image: quietPlaceDayOneImage,
    tags: ["movies", "horror", "thriller", "sci-fi"],
    reviews: [
      {
        id: 1,
        username: "CinematicCritic",
        rating: 3,
        title: "Visually Stunning but Narratively Thin",
        comment:
          "A Quiet Place: Day One builds tension well and features excellent sound design. However, the story and characters feel underdeveloped. While it offers some thrilling moments, it lacks the consistent suspense of its predecessors.",
      },
      {
        id: 2,
        username: "HorrorEnthusiast",
        rating: 4,
        title: "Solid Prequel with a Different Focus",
        comment:
          "This prequel shifts from horror to character drama, which might disappoint some fans. Nyong'o and Quinn deliver strong performances, and the film offers a unique perspective on the invasion. It's a refreshing take, even if it doesn't match the intensity of the original.",
      },
      {
        id: 3,
        username: "FilmBuff101",
        rating: 4,
        title: "Surprisingly Meditative",
        comment:
          "A beautiful, character-driven drama that occasionally reminds you it's a monster movie. Sarnoski's direction brings a fresh perspective to the franchise, with stunning visuals and emotional depth. It may not be what fans expect, but it's a compelling addition to the series.",
      },
      {
        id: 4,
        username: "ActionSeeker",
        rating: 2,
        title: "Too Quiet for Its Own Good",
        comment:
          "While the film boasts impressive visuals and sound design, it lacks the intense action and suspense of the previous installments. The focus on character development over alien encounters may disappoint those expecting a more thrilling experience. A missed opportunity to explore the initial invasion in depth.",
      },
    ],
    dateAdded: "2024-06-28T00:00:00Z",
    description:
      "This prequel to A Quiet Place follows a new set of characters as they navigate the terrifying first hours of the alien invasion that hunts by sound.",
  },
  {
    id: 19,
    title: "The Idea of You",
    price: 17.99,
    image: theIdeaOfYouImage,
    tags: ["movies", "romance", "drama", "comedy"],
    reviews: [
      {
        id: 1,
        username: "RomComEnthusiast",
        rating: 4,
        title: "Charming Romance with Stellar Performances",
        comment:
          "Anne Hathaway shines in this heartwarming rom-com, displaying her versatility and emotional depth. The chemistry between Hathaway and Nicholas Galitzine is palpable, making their on-screen romance believable and engaging. While the plot may follow familiar rom-com beats, the film's exploration of age-gap relationships and societal judgments adds a fresh perspective.",
      },
      {
        id: 2,
        username: "CriticalViewer",
        rating: 3,
        title: "Flawed but Entertaining",
        comment:
          "The Idea of You offers a mixed bag of delights and disappointments. Anne Hathaway's performance is a standout, but the script often feels clichéd and riddled with plot holes. The chemistry between the leads saves many scenes, yet the film struggles to fully capitalize on its premise. It's an enjoyable watch for rom-com fans, but don't expect groundbreaking cinema.",
      },
    ],
    dateAdded: "2024-05-02T00:00:00Z",
    description:
      "A 40-year-old single mom begins an unexpected romance with the 24-year-old lead singer of August Moon, the hottest boy band on the planet.",
  },
  {
    id: 20,
    title: "The Book of Clarence",
    price: 21.99,
    image: bookOfClarenceImage,
    tags: ["movies", "historical", "drama", "comedy"],
    reviews: [],
    dateAdded: "2024-01-12T00:00:00Z",
    description:
      "Set in 29 AD Jerusalem, this film follows Clarence, a down-on-his-luck man who embarks on a misguided attempt to capitalize on the rise of celebrity and influence surrounding the Messiah for his own personal gain.",
  },

  {
    id: 21,
    title: "Lenovo ThinkPad X1 Carbon Ultra",
    price: 2029.99,
    image: lenovoThinkPadX1CarbonUltraImage,
    tags: ["laptops", "business", "ultrabook", "high-performance", "14-inch"],
    reviews: [
      {
        id: 1,
        username: "TechPro",
        rating: 5,
        title: "Exceptional Performance",
        comment:
          "The Intel Core Ultra processor ensures seamless multitasking, and the OLED display is stunning.",
      },
      {
        id: 2,
        username: "OfficeGuru",
        rating: 4,
        title: "Great for Professionals",
        comment:
          "Amazing keyboard and long battery life, but slightly expensive.",
      },
      {
        id: 3,
        username: "TravelingExec",
        rating: 5,
        title: "Perfect Travel Companion",
        comment:
          "Lightweight, powerful, and reliable. It's my go-to for business trips.",
      },
      {
        id: 4,
        username: "BudgetBuyer",
        rating: 3,
        title: "Overpriced for Features",
        comment:
          "While it's a solid machine, the price point is hard to justify for the average user.",
      },
    ],
    dateAdded: "2024-11-01T00:00:00Z",
    description:
      "A high-performance laptop with Intel Core Ultra processors, AI-enhanced features, and a stunning 14-inch OLED display.",
  },
  {
    id: 22,
    title: "Lenovo Yoga Slim 7i Aura Edition",
    price: 999.99,
    image: lenovoYogaSlim7iImage,
    tags: [
      "laptops",
      "touchscreen",
      "creative",
      "high-performance",
      "15.3-inch",
    ],
    reviews: [
      {
        id: 1,
        username: "CreativeMind",
        rating: 5,
        title: "Perfect for Creatives",
        comment:
          "The 3K touchscreen and long battery life are ideal for design work.",
      },
      {
        id: 2,
        username: "CasualUser",
        rating: 4,
        title: "Stylish and Functional",
        comment:
          "Sleek design with great performance, but Wi-Fi setup was tricky.",
      },
      {
        id: 3,
        username: "TechSkeptic",
        rating: 2,
        title: "Disappointing Battery Life",
        comment:
          "The battery drains much faster than advertised, especially when using creative apps.",
      },
    ],
    dateAdded: "2024-10-15T00:00:00Z",
    description:
      "A sleek laptop with a vibrant touchscreen display and powerful performance for creators.",
  },
  {
    id: 23,
    title: "ASUS ZenBook Duo",
    price: 1299.99,
    image: asusZenbookDuoImage,
    tags: ["laptops", "dual-screen", "OLED", "high-performance", "14-inch"],
    reviews: [
      {
        id: 1,
        username: "Innovator101",
        rating: 5,
        title: "Game-Changing Design",
        comment: "The dual-screen setup is revolutionary for multitasking.",
      },
      {
        id: 2,
        username: "TechieGuy",
        rating: 4,
        title: "Impressive Features",
        comment:
          "Great performance but slightly bulky due to the dual screens.",
      },
      {
        id: 3,
        username: "ProductivityQueen",
        rating: 5,
        title: "Boost Your Workflow",
        comment:
          "The second screen is a game-changer for my productivity. Love it!",
      },
      {
        id: 4,
        username: "DesignerPro",
        rating: 4,
        title: "Great for Creative Work",
        comment:
          "The dual screens are perfect for design work, but the battery life could be better.",
      },
      {
        id: 5,
        username: "Skeptical123",
        rating: 3,
        title: "Interesting Concept, Flawed Execution",
        comment:
          "While the dual screens are innovative, the ergonomics can be awkward for extended use.",
      },
    ],
    dateAdded: "2024-09-28T00:00:00Z",
    description:
      "A dual-screen laptop with an OLED display and powerful specs for professionals.",
  },
  {
    id: 24,
    title: "Dell Inspiron 15",
    price: 629.99,
    image: dellInspiron15Image,
    tags: ["laptops", "budget", "FHD", "12th-gen-Intel", "15.6-inch"],
    reviews: [
      {
        id: 1,
        username: "ValueHunter",
        rating: 4,
        title: "Affordable and Reliable",
        comment:
          "Good performance for everyday tasks at a budget-friendly price.",
      },
      {
        id: 2,
        username: "StudentBudget",
        rating: 3,
        title: "Decent for the Price",
        comment:
          "It gets the job done for basic schoolwork, but don't expect anything fancy.",
      },
    ],
    dateAdded: "2024-08-20T00:00:00Z",
    description:
      "A budget-friendly laptop with solid performance for daily use.",
  },
  {
    id: 25,
    title: "Dell Inspiron Touch Laptop",
    price: 749.99,
    image: dellInspironTouchImage,
    tags: [
      "laptops",
      "2-in-1",
      "touchscreen",
      "FHD+",
      "13th-gen-Intel",
      "14-inch",
    ],
    reviews: [
      {
        id: 1,
        username: "FlexFan",
        rating: 5,
        title: "Versatile Design",
        comment: "The convertible modes are fantastic for work and play.",
      },
      {
        id: 2,
        username: "TabletConvert",
        rating: 4,
        title: "Great Hybrid Device",
        comment:
          "Excellent touchscreen functionality but slightly heavy for tablet mode.",
      },
      {
        id: 3,
        username: "StudentLife",
        rating: 5,
        title: "Perfect for College",
        comment:
          "The versatility is great for taking notes in class and watching movies in the dorm.",
      },
      {
        id: 4,
        username: "TechCritic",
        rating: 2,
        title: "Mediocre Performance",
        comment:
          "While the touch feature is nice, the overall performance is lacking for the price.",
      },
    ],
    dateAdded: "2024-07-10T00:00:00Z",
    description:
      "A versatile laptop with a flexible hinge and active pen support.",
  },
  {
    id: 26,
    title: "HP Spectre x360",
    price: 1399.99,
    image: hpSpectreX360Image,
    tags: ["laptops", "premium", "2-in-1", "high-performance", "13.5-inch"],
    reviews: [
      {
        id: 1,
        username: "LuxuryTech",
        rating: 5,
        title: "Premium Experience",
        comment:
          "The build quality and performance are top-notch. Worth every penny.",
      },
      {
        id: 2,
        username: "DesignEnthusiast",
        rating: 5,
        title: "Sleek and Powerful",
        comment:
          "Gorgeous design with the performance to match. The OLED screen is breathtaking.",
      },
      {
        id: 3,
        username: "PowerUser",
        rating: 4,
        title: "Almost Perfect",
        comment:
          "Great machine overall, but the fan noise can be noticeable under heavy loads.",
      },
    ],
    dateAdded: "2024-06-05T00:00:00Z",
    description:
      "A premium 2-in-1 laptop with a stunning design and powerful performance.",
  },
  {
    id: 27,
    title: "Acer Predator Helios 300",
    price: 1199.99,
    image: acerPredatorHelios300Image,
    tags: ["laptops", "gaming", "high-performance", "15.6-inch"],
    reviews: [
      {
        id: 1,
        username: "GamerPro",
        rating: 4,
        title: "Solid Gaming Performance",
        comment: "Great specs for the price, handles most games with ease.",
      },
      {
        id: 2,
        username: "TechEnthusiast",
        rating: 5,
        title: "Impressive Cooling",
        comment:
          "The cooling system is exceptional, keeping temperatures low even during intense gaming sessions.",
      },
      {
        id: 3,
        username: "CasualGamer",
        rating: 4,
        title: "Good Value",
        comment:
          "Powerful enough for my needs, but the fan noise can be a bit loud.",
      },
      {
        id: 4,
        username: "StreamerGirl",
        rating: 5,
        title: "Perfect for Streaming",
        comment:
          "Handles gaming and streaming simultaneously without breaking a sweat.",
      },
      {
        id: 5,
        username: "BatteryConscious",
        rating: 3,
        title: "Poor Battery Life",
        comment:
          "Great performance when plugged in, but battery life is abysmal for on-the-go use.",
      },
    ],
    dateAdded: "2024-05-20T00:00:00Z",
    description:
      "A high-performance gaming laptop with advanced cooling technology.",
  },
  {
    id: 28,
    title: "Microsoft Surface Laptop 5",
    price: 999.99,
    image: microsoftSurfaceLaptop5Image,
    tags: [
      "laptops",
      "ultraportable",
      "touchscreen",
      "high-performance",
      "13.5-inch",
    ],
    reviews: [
      {
        id: 1,
        username: "MinimalistUser",
        rating: 5,
        title: "Sleek and Efficient",
        comment:
          "The clean design and smooth performance make this my favorite laptop.",
      },
      {
        id: 2,
        username: "WindowsFan",
        rating: 4,
        title: "Great Windows Experience",
        comment:
          "Seamless integration with Windows 11, but I wish it had more ports.",
      },
      {
        id: 3,
        username: "PortabilityFirst",
        rating: 5,
        title: "Ultimate Portability",
        comment:
          "So light and compact, it's perfect for my on-the-go lifestyle.",
      },
    ],
    dateAdded: "2024-04-15T00:00:00Z",
    description:
      "An elegant and lightweight laptop with a vibrant PixelSense touchscreen.",
  },
  {
    id: 29,
    title: "Apple MacBook Air M3",
    price: 1299.99,
    image: appleMacBookAirM3Image,
    tags: [
      "laptops",
      "macOS",
      "ultraportable",
      "high-performance",
      "13.6-inch",
    ],
    reviews: [
      {
        id: 1,
        username: "AppleEnthusiast",
        rating: 5,
        title: "Incredible Performance",
        comment:
          "The M3 chip is a game-changer. Blazing fast with amazing battery life.",
      },
      {
        id: 2,
        username: "DesignerPro",
        rating: 5,
        title: "Perfect for Creatives",
        comment:
          "The color accuracy and performance make it ideal for design work.",
      },
      {
        id: 3,
        username: "TechReviewer",
        rating: 4,
        title: "Almost Perfect",
        comment:
          "Fantastic machine, but the lack of ports can be limiting for some users.",
      },
      {
        id: 4,
        username: "WindowsConverter",
        rating: 5,
        title: "Convinced Me to Switch",
        comment:
          "As a long-time Windows user, this laptop convinced me to switch to Mac. It's that good.",
      },
    ],
    dateAdded: "2024-03-01T00:00:00Z",
    description:
      "The latest MacBook Air featuring the powerful M3 chip and a brilliant Retina display.",
  },
  {
    id: 30,
    title: "Razer Blade 15",
    price: 1799.99,
    image: razerBlade15Image,
    tags: ["laptops", "gaming", "premium", "high-performance", "15.6-inch"],
    reviews: [
      {
        id: 1,
        username: "ProGamer",
        rating: 5,
        title: "Desktop Replacement",
        comment:
          "Incredible performance in a sleek package. Handles all my games at max settings.",
      },
      {
        id: 2,
        username: "TechNerd",
        rating: 4,
        title: "Powerful but Pricey",
        comment:
          "Top-tier performance and build quality, but it comes at a premium price.",
      },
      {
        id: 3,
        username: "DesignGuru",
        rating: 5,
        title: "Perfect for Work and Play",
        comment:
          "Powerful enough for 3D rendering and gaming. The display is phenomenal.",
      },
      {
        id: 4,
        username: "Traveler101",
        rating: 4,
        title: "Portable Powerhouse",
        comment:
          "Great performance in a relatively compact body, but battery life could be better.",
      },
      {
        id: 5,
        username: "BudgetGamer",
        rating: 2,
        title: "Overpriced for Average Users",
        comment:
          "While it's a beast, the price is hard to justify unless you're a serious gamer or professional.",
      },
    ],
    dateAdded: "2024-02-10T00:00:00Z",
    description:
      "A premium gaming laptop with a sleek design and top-of-the-line performance.",
  },
  {
    id: 31,
    title: "RayBan Aviator Classic",
    price: 154.99,
    image: raybanAviatorImage,
    tags: ["sunglasses", "classic", "aviator", "metal-frame", "UV-protection"],
    reviews: [
      {
        id: 1,
        username: "SunnyDays",
        rating: 5,
        title: "Timeless Style",
        comment:
          "These aviators never go out of fashion. Great quality and comfortable fit.",
      },
      {
        id: 2,
        username: "BeachLover",
        rating: 4,
        title: "Good, but pricey",
        comment:
          "Love the look, but they're a bit expensive for what they are.",
      },
      {
        id: 3,
        username: "FashionIcon",
        rating: 5,
        title: "Must-have accessory",
        comment: "These sunglasses elevate any outfit. Worth every penny!",
      },
    ],
    dateAdded: "2024-01-15T00:00:00Z",
    description:
      "The iconic RayBan Aviator, offering timeless style and 100% UV protection.",
  },
  {
    id: 32,
    title: "Oakley Holbrook",
    price: 126.0,
    image: oakleyHolbrookImage,
    tags: ["sunglasses", "sports", "rectangular", "plastic-frame", "polarized"],
    reviews: [
      {
        id: 1,
        username: "SportsFanatic",
        rating: 5,
        title: "Perfect for outdoor activities",
        comment:
          "These Oakleys are great for sports. The polarized lenses really make a difference.",
      },
      {
        id: 2,
        username: "CasualWearer",
        rating: 4,
        title: "Stylish and functional",
        comment: "Good looking glasses that work well for everyday use.",
      },
      {
        id: 3,
        username: "SkepticalBuyer",
        rating: 2,
        title: "Not as durable as expected",
        comment:
          "They look great but scratched easily after a few weeks of use.",
      },
    ],
    dateAdded: "2024-01-20T00:00:00Z",
    description:
      "Oakley Holbrook sunglasses combine style with high-performance polarized lenses.",
  },
  {
    id: 33,
    title: "Persol 714",
    price: 380.0,
    image: persol714Image,
    tags: ["sunglasses", "luxury", "folding", "acetate-frame", "Italian"],
    reviews: [
      {
        id: 1,
        username: "LuxuryLover",
        rating: 5,
        title: "Exquisite craftsmanship",
        comment:
          "These Persols are a work of art. The folding mechanism is so smooth.",
      },
      {
        id: 2,
        username: "DisappointedCustomer",
        rating: 3,
        title: "Beautiful but fragile",
        comment:
          "They look amazing but feel a bit flimsy. Not sure how long they'll last.",
      },
    ],
    dateAdded: "2024-02-01T00:00:00Z",
    description:
      "The Persol 714, a folding version of the iconic model, exudes Italian luxury.",
  },
  {
    id: 34,
    title: "Warby Parker Haskell",
    price: 95.0,
    image: warbyParkerHaskellImage,
    tags: [
      "sunglasses",
      "affordable",
      "round",
      "acetate-frame",
      "prescription-ready",
    ],
    reviews: [
      {
        id: 1,
        username: "BudgetBuyer",
        rating: 5,
        title: "Great value",
        comment:
          "These glasses look much more expensive than they are. Love the style!",
      },
      {
        id: 2,
        username: "HipsterChic",
        rating: 4,
        title: "Cool design",
        comment:
          "The round shape is very on-trend. Comfortable to wear all day.",
      },
      {
        id: 3,
        username: "QualitySeeker",
        rating: 3,
        title: "Decent for the price",
        comment: "Not bad, but the build quality could be better.",
      },
      {
        id: 4,
        username: "StyleNovice",
        rating: 5,
        title: "My go-to glasses",
        comment: "These have become my everyday sunglasses. So versatile!",
      },
    ],
    dateAdded: "2024-02-05T00 :00 :00Z",
    description:
      "Warby Parker Haskell offers trendy round frames at an affordable price point.",
  },
  {
    id: 35,
    title: "Maui Jim Red Sands",
    price: 249.99,
    image: mauiJimRedSandsImage,
    tags: ["sunglasses", "polarized", "rectangular", "nylon-frame", "beach"],
    reviews: [
      {
        id: 1,
        username: "IslandHopper",
        rating: 5,
        title: "Perfect for tropical getaways",
        comment:
          "These Maui Jims are amazing for beach days. The clarity is unreal.",
      },
      {
        id: 2,
        username: "SunProtector",
        rating: 5,
        title: "Best lenses I've tried",
        comment:
          "The polarization on these is top-notch. Worth the investment.",
      },
    ],
    dateAdded: "2024-02-10T00 :00 :00Z",
    description:
      "Maui Jim Red Sands features advanced polarized lenses perfect for bright sunny days.",
  },
  {
    id: 36,
    title: "Gucci GG0022S",
    price: 375.0,
    image: gucciGG0022SImage,
    tags: ["sunglasses", "designer", "oversized", "acetate-frame", "luxury"],
    reviews: [
      {
        id: 1,
        username: "FashionForward",
        rating: 5,
        title: "Statement piece",
        comment:
          "These Gucci sunglasses make me feel like a celebrity. Love the oversized look.",
      },
      {
        id: 2,
        username: "DisappointedDiva",
        rating: 2,
        title: "Not worth the hype",
        comment:
          "They look great but are uncomfortable to wear for long periods.",
      },
    ],
    dateAdded: "2024-02-15T00 :00 :00Z",
    description:
      "Gucci GG0022S offers bold oversized frames for those who want to make a statement.",
  },
  {
    id: 37,
    title: "Costa Del Mar Fantail",
    price: 189.0,
    image: costaDelMarFantailImage,
    tags: [
      "sunglasses",
      "fishing",
      "wrap-around",
      "polycarbonate-frame",
      "water-resistant",
    ],
    reviews: [
      {
        id: 1,
        username: "FishingPro",
        rating: 5,
        title: "Best for on the water",
        comment:
          "These Costas are perfect for fishing. Great glare reduction and they stay put.",
      },
      {
        id: 2,
        username: "WeekendAngler",
        rating: 4,
        title: "Solid choice",
        comment:
          "Good glasses for the price. Comfortable for long days out on the boat.",
      },
      {
        id: 3,
        username: "OutdoorEnthusiast",
        rating: 5,
        title: "Versatile performance",
        comment:
          "Not just for fishing - these are great for any outdoor activity.",
      },
    ],
    dateAdded: "2024-02-20T00 :00 :00Z",
    description:
      "Costa Del Mar Fantail sunglasses are designed for optimal performance in and around water.",
  },
  {
    id: 38,
    title: "Prada PR01OS",
    price: 290.0,
    image: pradaPR01OSImage,
    tags: [
      "sunglasses",
      "designer",
      "cat-eye",
      "metal-frame",
      "gradient-lenses",
    ],
    reviews: [
      {
        id: 1,
        username: "GlamGirl",
        rating: 5,
        title: "Absolutely stunning",
        comment:
          "These Prada sunglasses are gorgeous. The cat-eye shape is so flattering.",
      },
      {
        id: 2,
        username: "FashionCritic",
        rating: 4,
        title: "Chic but delicate",
        comment:
          "Beautiful design, but be careful with them as they're quite delicate.",
      },
    ],
    dateAdded: "2024-02-25T00 :00 :00Z",
    description:
      "Prada PR01OS features a stylish cat-eye design with luxurious gradient lenses.",
  },
  {
    id: 39,
    title: "Smith Optics Lowdown II",
    price: 129.0,
    image: smithOpticsLowdown2Image,
    tags: [
      "sunglasses",
      "sports",
      "square",
      "eco-friendly",
      "impact-resistant",
    ],
    reviews: [
      {
        id: 1,
        username: "EcoWarrior",
        rating: 5,
        title: "Sustainable and stylish",
        comment:
          "Love that these are made from recycled materials. They look great too!",
      },
      {
        id: 2,
        username: "AdventureSeeker",
        rating: 4,
        title: "Durable and comfortable",
        comment:
          "These have held up well during my outdoor adventures. Good value.",
      },
      {
        id: 3,
        username: "CasualExplorer",
        rating: 5,
        title: "Versatile choice",
        comment:
          "Great for both city wear and outdoor activities. Highly recommend.",
      },
      {
        id: 4,
        username: "StyleConscious",
        rating: 3,
        title: "Functional but plain",
        comment: "They work well but the design is a bit boring for my taste.",
      },
      {
        id: 5,
        username: "SunnyDayHiker",
        rating: 2,
        title: "Not as good as expected",
        comment:
          "They feel cheap and don't provide enough UV protection in bright sunlight.",
      },
    ],
    dateAdded: "2024-03-01T00 :00 :00Z",
    description:
      "Smith Optics Lowdown II combines eco-friendly materials with durable sporty design.",
  },
  {
    id: 40,
    title: "Dior DiorSoReal",
    price: 495.0,
    image: diorSoRealImage,
    tags: [
      "sunglasses",
      "luxury",
      "avant-garde",
      "metal-frame",
      "mirrored-lenses",
    ],
    reviews: [
      {
        id: 1,
        username: "FashionForward",
        rating: 5,
        title: "Futuristic and fabulous",
        comment:
          "These Dior sunglasses are a work of art. Always get compliments when I wear them.",
      },
    ],
    dateAdded: "2024-03-05T00 :00 :00Z",
    description:
      "Dior DiorSoReal offers an avant-garde design with striking mirrored lenses for the fashion-forward.",
  },
  {
    id: 41,
    title: "Hydro Flask Wide Mouth",
    price: 44.95,
    image: hydroFlaskImage,
    tags: [
      "water bottles",
      "insulated",
      "stainless-steel",
      "wide-mouth",
      "durable",
    ],
    reviews: [
      {
        id: 1,
        username: "HydrationFanatic",
        rating: 5,
        title: "Best bottle ever!",
        comment: "Keeps my water cold for hours, even in hot weather. Love it!",
      },
      {
        id: 2,
        username: "OutdoorExplorer",
        rating: 5,
        title: "Reliable companion",
        comment: "Perfect for hiking trips. Sturdy and doesn't leak.",
      },
      {
        id: 3,
        username: "GymRat",
        rating: 4,
        title: "Great but pricey",
        comment:
          "Excellent quality, but a bit expensive. Still worth it though.",
      },
    ],
    dateAdded: "2024-01-10T00:00:00Z",
    description:
      "The Hydro Flask Wide Mouth keeps beverages cold for up to 24 hours or hot for up to 12 hours.",
  },
  {
    id: 42,
    title: "Nalgene Tritan Wide Mouth",
    price: 14.99,
    image: nalgeneImage,
    tags: [
      "water bottles",
      "Bpa-free",
      "wide-mouth",
      "lightweight",
      "affordable",
    ],
    reviews: [
      {
        id: 1,
        username: "BudgetBuyer",
        rating: 5,
        title: "Unbeatable value",
        comment:
          "Affordable, durable, and gets the job done. What more could you want?",
      },
      {
        id: 2,
        username: "CampingEnthusiast",
        rating: 4,
        title: "Reliable classic",
        comment: "Been using Nalgene for years. This one doesn't disappoint.",
      },
    ],
    dateAdded: "2024-01-15T00:00:00Z",
    description:
      "The classic Nalgene Tritan Wide Mouth is a durable and affordable option for everyday hydration.",
  },
  {
    id: 43,
    title: "S'well Stainless Steel Water Bottle",
    price: 35.0,
    image: swellImage,
    tags: [
      "water bottles",
      "insulated",
      "stainless-steel",
      "stylish",
      "leak-proof",
    ],
    reviews: [
      {
        id: 1,
        username: "FashionForward",
        rating: 5,
        title: "Stylish and functional",
        comment:
          "Love the designs! Keeps my drinks at the perfect temperature.",
      },
      {
        id: 2,
        username: "OfficeDweller",
        rating: 4,
        title: "Great for work",
        comment:
          "Fits nicely on my desk and in my bag. Wish it had a wider mouth for easy cleaning.",
      },
      {
        id: 3,
        username: "EcoWarrior",
        rating: 5,
        title: "Eco-friendly choice",
        comment:
          "Helped me ditch single-use plastic bottles. Highly recommend!",
      },
      {
        id: 4,
        username: "YogaLover",
        rating: 3,
        title: "Pretty but heavy",
        comment:
          "Beautiful bottle, but a bit heavy for carrying to yoga class.",
      },
    ],
    dateAdded: "2024-01-20T00:00:00Z",
    description:
      "S'well bottles combine fashion with function, offering stylish designs and excellent insulation.",
  },
  {
    id: 44,
    title: "CamelBak Eddy+",
    price: 15.0,
    image: camelBakEddyImage,
    tags: [
      "water bottles",
      "Bpa-free",
      "spill-proof",
      "dishwasher-safe",
      "bite-valve",
    ],
    reviews: [
      {
        id: 1,
        username: "BusyMom",
        rating: 5,
        title: "Perfect for kids",
        comment: "The bite valve is great for my toddler. No more spills!",
      },
      {
        id: 2,
        username: "DeskJockey",
        rating: 4,
        title: "Good for sipping",
        comment:
          "I like that I can sip without tipping the bottle. Wish it was insulated though.",
      },
    ],
    dateAdded: "2024-01-25T00:00:00Z",
    description:
      "The CamelBak Eddy+ features a spill-proof bite valve for easy sipping on the go.",
  },
  {
    id: 45,
    title: "Yeti Rambler",
    price: 39.99,
    image: yetiRamblerImage,
    tags: [
      "water bottles",
      "insulated",
      "stainless-steel",
      "dishwasher-safe",
      "durable",
    ],
    reviews: [
      {
        id: 1,
        username: "OutdoorsMan",
        rating: 5,
        title: "Built to last",
        comment: "This thing is indestructible! Keeps ice frozen for days.",
      },
      {
        id: 2,
        username: "BeachBum",
        rating: 5,
        title: "Beach essential",
        comment: "Perfect for long days in the sun. Doesn't sweat or leak.",
      },
      {
        id: 3,
        username: "RoadTripper",
        rating: 4,
        title: "Great but bulky",
        comment:
          "Excellent insulation, but takes up a lot of cup holder space.",
      },
    ],
    dateAdded: "2024-01-30T00:00:00Z",
    description:
      "The Yeti Rambler offers superior insulation and durability for extreme conditions.",
  },
  {
    id: 46,
    title: "Contigo Autoseal West Loop",
    price: 24.99,
    image: contigoWestLoopImage,
    tags: [
      "water bottles",
      "insulated",
      "stainless-steel",
      "autoseal",
      "leak-proof",
    ],
    reviews: [
      {
        id: 1,
        username: "CommuteCrusader",
        rating: 5,
        title: "Perfect for commuting",
        comment:
          "The autoseal feature is a game-changer. No more spills in my bag!",
      },
      {
        id: 2,
        username: "CoffeeAddict",
        rating: 4,
        title: "Great for hot drinks",
        comment:
          "Keeps my coffee hot for hours. Wish it was easier to clean though.",
      },
    ],
    dateAdded: "2024-02-05T00:00:00Z",
    description:
      "The Contigo Autoseal West Loop features a unique autoseal mechanism to prevent leaks and spills.",
  },
  {
    id: 47,
    title: "Klean Kanteen Classic",
    price: 29.95,
    image: kleanKanteenClassicImage,
    tags: [
      "water bottles",
      "stainless-steel",
      "eco-friendly",
      "durable",
      "wide-mouth",
    ],
    reviews: [
      {
        id: 1,
        username: "EcoWarrior",
        rating: 5,
        title: "Sustainable choice",
        comment:
          "Love that it's plastic-free and built to last. Great company ethics too!",
      },
      {
        id: 2,
        username: "MinimalistTraveler",
        rating: 4,
        title: "Simple and effective",
        comment:
          "No frills, just a solid water bottle. Bit prone to dents though.",
      },
      {
        id: 3,
        username: "HealthNut",
        rating: 5,
        title: "Clean taste",
        comment:
          "No metallic taste like some other bottles. Easy to clean too!",
      },
    ],
    dateAdded: "2024-02-10T00:00:00Z",
    description:
      "The Klean Kanteen Classic is a durable, eco-friendly option made from high-quality stainless steel.",
  },
  {
    id: 48,
    title: "Takeya Actives Insulated Water Bottle",
    price: 34.99,
    image: takeyaActivesImage,
    tags: [
      "water bottles",
      "insulated",
      "stainless-steel",
      "spout-lid",
      "sweat-free",
    ],
    reviews: [
      {
        id: 1,
        username: "FitnessFreak",
        rating: 5,
        title: "Gym essential",
        comment:
          "The spout lid is perfect for quick sips during workouts. Keeps water cold for hours!",
      },
      {
        id: 2,
        username: "HotYogaFan",
        rating: 4,
        title: "Great but heavy",
        comment:
          "Excellent insulation, but a bit heavy for carrying to yoga class.",
      },
    ],
    dateAdded: "2024-02-15T00:00:00Z",
    description:
      "Takeya Actives bottle features a unique spout lid design and excellent insulation for active lifestyles.",
  },
  {
    id: 49,
    title: "Brita Premium Filtering Water Bottle",
    price: 19.99,
    image: britaFilterBottleImage,
    tags: [
      "water bottles",
      "filtered",
      "Bpa-free",
      "leak-proof",
      "dishwasher-safe",
    ],
    reviews: [
      {
        id: 1,
        username: "WaterSnob",
        rating: 5,
        title: "Clean taste anywhere",
        comment:
          "Great for travel or areas with questionable tap water. Noticeable improvement in taste.",
      },
      {
        id: 2,
        username: "GymGoer",
        rating: 3,
        title: "Good concept, okay execution",
        comment:
          "Like the filter idea, but flow rate is slow and filters need frequent replacement.",
      },
      {
        id: 3,
        username: "HealthConsciousParent",
        rating: 4,
        title: "Peace of mind",
        comment: "Feel better about my kids drinking filtered water at school.",
      },
    ],
    dateAdded: "2024-02-20T00:00:00Z",
    description:
      "The Brita Premium Filtering Water Bottle lets you enjoy crisp, filtered water on the go.",
  },
  {
    id: 50,
    title: "Lifefactory Glass Water Bottle",
    price: 22.99,
    image: lifefactoryGlassBottleImage,
    tags: [
      "water bottles",
      "glass",
      "silicone-sleeve",
      "dishwasher-safe",
      "eco-friendly",
    ],
    reviews: [
      {
        id: 1,
        username: "PlasticFreeLife",
        rating: 5,
        title: "Love the glass!",
        comment:
          "No plastic taste, easy to clean, and the silicone sleeve provides good protection.",
      },
      {
        id: 2,
        username: "YogaInstructor",
        rating: 4,
        title: "Beautiful but fragile",
        comment:
          "Looks great and love drinking from glass, but need to be careful not to drop it.",
      },
    ],
    dateAdded: "2024-02-25T00:00:00Z",
    description:
      "Lifefactory Glass Water Bottle offers a pure taste with a protective silicone sleeve for durability.",
  },
  {
    id: 51,
    title: "Colgate Gentle Care Toothbrush",
    price: 3.99,
    image: colgateToothBrushImage,
    tags: ["toothbrush", "dental care", "sensodyne"],
    reviews: [
      {
        id: 1,
        username: "ToothFan",
        rating: 4,
        title: "Great for sensitive teeth",
        comment:
          "I love how gentle yet effective this toothbrush is on my sensitive gums. It delivers a clean feeling without being harsh.",
      },
    ],
    dateAdded: "2024-11-15T00:00:00Z",
    description:
      "A soft-bristled toothbrush designed for sensitive teeth, ensuring a gentle yet effective clean."
  },
  {
    id: 52,
    title: "Generic UltraSoft Toothbrush",
    price: 4.99,
    image: genericToothBrushImage,
    tags: ["toothbrush", "dental care", "sensodyne"],
    reviews: [
      {
        id: 1,
        username: "BestBrushEver",
        rating: 5,
        title: "Exceptional comfort and cleaning",
        comment:
          "This toothbrush exceeded all my expectations with its ultra-soft bristles and thorough cleaning power. Highly recommended!",
      },
    ],
    dateAdded: "2024-11-15T00:00:00Z",
    description:
      "Featuring ultra-sensitive bristles, this toothbrush offers superior cleaning while protecting your gums."
  },
  {
    id: 53,
    title: "Sensodyne ProClean Toothbrush",
    price: 5.99,
    image: sensodyneToothBrushImage,
    tags: ["toothbrush", "dental care", "sensodyne"],
    reviews: [
      {
        id: 1,
        username: "NotImpressed",
        rating: 1,
        title: "Disappointing performance",
        comment:
          "I was really disappointed with this toothbrush. The cleaning is subpar and it feels uncomfortable. I expected much more from a Sensodyne product.",
      },
    ],
    dateAdded: "2024-11-16T00:00:00Z",
    description:
      "A toothbrush featuring advanced cleaning bristles for a thorough dental care routine.",
  },
  {
    id: 54,
    title: "Oral-B Precision Clean Toothbrush",
    price: 4.49,
    image: oralBToothBrushImage,
    tags: ["toothbrush", "dental care", "oralB"],
    reviews: [
      {
        id: 1,
        username: "CleanTeeth",
        rating: 4,
        title: "Reliable and effective",
        comment:
          "A solid toothbrush that consistently leaves my mouth feeling fresh and clean. It’s a dependable choice for everyday dental care.",
      },
    ],
    dateAdded: "2024-11-20T00:00:00Z",
    description:
      "A high-quality toothbrush from Oral-B designed for precision cleaning and optimal dental care."
  },
];

export default sampleProducts;
