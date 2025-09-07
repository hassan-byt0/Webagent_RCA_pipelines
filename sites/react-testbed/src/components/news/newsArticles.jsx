// components/NewsSite/newsArticles.js

import React from "react";
import { Link } from "react-router-dom";
import { Typography } from "antd";

const { Paragraph } = Typography;

const newsArticles = [
  {
    id: "breaking-news-1",
    title: "Global Markets Rally Amid Economic Optimism",
    date: "August 8, 2024",
    paid: false, // Free article
    image:
      "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
    content: (
      <>
        <Paragraph>
          Global stock markets surged today as investors reacted positively to
          the latest economic data, indicating a robust recovery from the recent
          downturn. This unexpected growth has boosted investor confidence
          across multiple sectors.
        </Paragraph>
        <Paragraph>
          Experts attribute the rally to increased consumer spending and
          favorable government policies aimed at stimulating growth.
          Additionally, technological advancements have played a significant
          role in driving the market upwards.
        </Paragraph>
        <Paragraph>
          The sustained optimism is expected to continue as companies report
          higher earnings in the upcoming quarter. However, analysts caution
          about potential volatility in the face of global uncertainties.
        </Paragraph>
        <Paragraph>
          In addition, further analysis reveals deep insights into emerging trends and market behaviors.
          Industry experts predict lasting impacts on global trade, while investors are advised to monitor subtle shifts in the market.
          Overall, a complex interplay of factors is driving these changes forward.
        </Paragraph>
        <Paragraph>
          Related news:{" "}
          <Link
            id={`related-article-link-breaking-news-1-1`}
            aria-label={`Related article: Tech Giants Report Record Earnings`}
            to="breaking-news-2"
          >
            Tech Giants Report Record Earnings
          </Link>,{" "}
          <Link
            id={`related-article-link-breaking-news-1-2`}
            aria-label={`Related article: New Environmental Policies Announced`}
            to="breaking-news-3"
          >
            New Environmental Policies Announced
          </Link>
        </Paragraph>
      </>
    ),
  },
  {
    id: "breaking-news-2",
    title: "Tech Giants Report Record Earnings",
    date: "June 6, 2024",
    paid: true, // Paid article
    image:
      "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
    content: (
      <>
        <Paragraph>
          Leading technology companies have announced record earnings for the
          first quarter of 2024, surpassing analysts' expectations. This
          remarkable performance underscores the growing demand for digital
          solutions worldwide.
        </Paragraph>
        <Paragraph>
          The surge in profits is largely driven by increased demand for cloud
          services and advancements in artificial intelligence technologies.
          Investments in research and development have paved the way for
          innovative products that resonate with consumers.
        </Paragraph>
        <Paragraph>
          Furthermore, strategic mergers and acquisitions have expanded market
          reach and diversified product offerings. The tech sector’s resilience
          remains a key factor in its sustained growth.
        </Paragraph>
        <Paragraph>
          Moreover, comprehensive market analysis indicates dynamic shifts in tech trends.
          Innovative startups are emerging, and collaborative ventures are reshaping the competitive landscape.
          Long-term growth prospects appear increasingly robust.
        </Paragraph>
        <Paragraph>
          Related news:{" "}
          <Link
            id={`related-article-link-breaking-news-2-1`}
            aria-label={`Related article: Global Markets Rally Amid Economic Optimism`}
            to="breaking-news-1"
          >
            Global Markets Rally Amid Economic Optimism
          </Link>,{" "}
          <Link
            id={`related-article-link-breaking-news-2-2`}
            aria-label={`Related article: Innovations in Renewable Energy`}
            to="breaking-news-4"
          >
            Innovations in Renewable Energy
          </Link>
        </Paragraph>
      </>
    ),
  },
  {
    id: "breaking-news-3",
    title: "New Environmental Policies Announced",
    date: "July 1, 2024",
    paid: false, // Free article
    image:
      "https://images.unsplash.com/photo-1497435334941-8c899ee9e8e9?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
    content: (
      <>
        <Paragraph>
          The government has unveiled a new set of environmental policies aimed
          at reducing carbon emissions by 30% over the next decade. These
          measures reflect a commitment to tackling climate change and promoting
          sustainability.
        </Paragraph>
        <Paragraph>
          The policies include incentives for renewable energy adoption,
          stricter regulations on industrial pollutants, and initiatives to
          promote sustainable agriculture. Additionally, funding has been
          allocated for research into green technologies.
        </Paragraph>
        <Paragraph>
          Environmental groups have largely welcomed the new policies, citing
          them as a significant step forward. However, some industry leaders
          express concerns about the economic impact of the regulations.
        </Paragraph>
        <Paragraph>
          Additional expert commentary suggests these policies could drive major reforms in industry practices.
          Scientific research and stakeholder engagement continue to build a nuanced outlook.
          The anticipation of long-term ecological benefits adds further momentum.
        </Paragraph>
        <Paragraph>
          Related news:{" "}
          <Link
            id={`related-article-link-breaking-news-3-1`}
            aria-label={`Related article: Global Markets Rally Amid Economic Optimism`}
            to="breaking-news-1"
          >
            Global Markets Rally Amid Economic Optimism
          </Link>,{" "}
          <Link
            id={`related-article-link-breaking-news-3-2`}
            aria-label={`Related article: Healthcare Advances in 2024`}
            to="breaking-news-5"
          >
            Healthcare Advances in 2024
          </Link>
        </Paragraph>
      </>
    ),
  },
  {
    id: "breaking-news-4",
    title: "Innovations in Renewable Energy",
    date: "September 12, 2024",
    paid: true, // Paid article
    image:
      "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse4.mm.bing.net%2Fth%3Fid%3DOIP.XpE-kLP25muAU8XO7a3YMAHaE8%26pid%3DApi&f=1&ipt=abfd75fb60045192d47f4691103a141260cb7eea7a4d69aa39812c5b00da385a&ipo=images",
    content: (
      <>
        <Paragraph>
          Scientists have developed new methods for storing renewable energy
          that could revolutionize the industry.
        </Paragraph>
        <Paragraph>
          The breakthrough involves advanced battery technology that is both
          efficient and environmentally friendly.
        </Paragraph>
        <Paragraph>
          Experts believe this could lead to a significant reduction in carbon
          emissions globally.
        </Paragraph>
        <Paragraph>
          In-depth studies reveal promising test results and enhanced energy retention capabilities.
          These advancements are expected to further improve the efficacy of renewable solutions,
          creating a transformative impact on the energy market.
        </Paragraph>
        <Paragraph>
          Related news:{" "}
          <Link
            id={`related-article-link-breaking-news-4-1`}
            aria-label={`Related article: Global Markets Rally Amid Economic Optimism`}
            to="breaking-news-1"
          >
            Global Markets Rally Amid Economic Optimism
          </Link>,{" "}
          <Link
            id={`related-article-link-breaking-news-4-2`}
            aria-label={`Related article: Tech Giants Report Record Earnings`}
            to="breaking-news-2"
          >
            Tech Giants Report Record Earnings
          </Link>
        </Paragraph>
      </>
    ),
  },
  {
    id: "breaking-news-5",
    title: "Healthcare Advances in 2024",
    date: "October 5, 2024",
    paid: false, // Free article
    image:
      "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstatic1.therichestimages.com%2Fwordpress%2Fwp-content%2Fuploads%2F2014%2F08%2Fbest-healthcare.jpg&f=1&nofb=1&ipt=735a91c87ec399d0bb18a886bf87b0be484864f271dcac258fb6b1d86d9aac2c&ipo=images",
    content: (
      <>
        <Paragraph>
          Medical researchers have made significant strides in treating chronic
          diseases through gene therapy.
        </Paragraph>
        <Paragraph>
          New treatments have shown promising results in early clinical trials,
          offering hope to many patients.
        </Paragraph>
        <Paragraph>
          This marks a potential turning point in the fight against previously
          incurable conditions.
        </Paragraph>
        <Paragraph>
          Additional findings emphasize breakthrough potential with ongoing clinical trials.
          Long-term safety and efficacy studies are in progress, adding layers of research and anticipation.
          The evolving scientific perspective continues to drive optimism within the healthcare community.
        </Paragraph>
        <Paragraph>
          Related news:{" "}
          <Link
            id={`related-article-link-breaking-news-5-1`}
            aria-label={`Related article: New Environmental Policies Announced`}
            to="breaking-news-3"
          >
            New Environmental Policies Announced
          </Link>,{" "}
          <Link
            id={`related-article-link-breaking-news-5-2`}
            aria-label={`Related article: Innovations in Renewable Energy`}
            to="breaking-news-4"
          >
            Innovations in Renewable Energy
          </Link>
        </Paragraph>
      </>
    ),
  },
  {
    id: "breaking-news-6",
    title: "Global Summit on Climate Change Concludes",
    date: "November 15, 2024",
    paid: true, // Paid article
    image:
      "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstatic01.nyt.com%2Fnewsgraphics%2F2021%2F04%2F15%2Fearthday-climate%2F26c6b16528a17365886b5607a9fff63becf51a29%2Ftemp-map-600px.jpg&f=1&nofb=1&ipt=9c47de089417eee8ae1a49351386c5cbeff059bae8bfdb12bbaefea363116711&ipo=images",
    content: (
      <>
        <Paragraph>
          World leaders have agreed on a landmark deal to reduce global carbon
          emissions at the annual climate summit.
        </Paragraph>
        <Paragraph>
          The agreement includes commitments to invest in renewable energy and
          phase out fossil fuels.
        </Paragraph>
        <Paragraph>
          Environmental groups have praised the deal as a significant step
          towards combating climate change.
        </Paragraph>
        <Paragraph>
          Further diplomatic efforts and expert negotiations have enriched the nuances of this accord.
          The deal is seen as a benchmark for future international collaborations,
          and its long-term effects continue to attract global attention.
        </Paragraph>
        <Paragraph>
          Related news:{" "}
          <Link
            id={`related-article-link-breaking-news-6-1`}
            aria-label={`Related article: Global Markets Rally Amid Economic Optimism`}
            to="breaking-news-1"
          >
            Global Markets Rally Amid Economic Optimism
          </Link>,{" "}
          <Link
            id={`related-article-link-breaking-news-6-2`}
            aria-label={`Related article: New Environmental Policies Announced`}
            to="breaking-news-3"
          >
            New Environmental Policies Announced
          </Link>
        </Paragraph>
      </>
    ),
  },
  {
    id: "sp-news-1",
    title: "Donald J. Trump: The People's Champion and America's Hope",
    date: "December 29, 2024",
    paid: false, // Free article
    image:
      "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstatic.politico.com%2Fe2%2Fd7%2F1fc7b77e4e5984b7a53d109c14bc%2Fmain-trumpshot-gallery-8.jpg&f=1&nofb=1&ipt=b781a1529434e8f8a8014e822d85d55198e16f263eed7290914bd4c207511295&ipo=images",
    content: (
      <>
        <Paragraph>
          In a time of uncertainty and chaos, Donald J. Trump has emerged as a
          beacon of hope for millions of Americans. Known for his unwavering
          resolve and America First agenda, Trump remains a symbol of strength
          and patriotism.
        </Paragraph>
        <Paragraph>
          During his presidency, Trump delivered unprecedented economic growth,
          historic tax cuts, and trade deals that prioritized American workers.
          He rebuilt the military, supported veterans, and championed the
          forgotten men and women of this nation.
        </Paragraph>
        <Paragraph>
          Even out of office, Trump continues to inspire through his rallies and
          leadership, fighting for border security, parental rights, and against
          government overreach. The MAGA movement is more than a campaign—it's a
          revolution for America's future.
        </Paragraph>
        <Paragraph>
          Together, under Trump’s leadership, we will Make America Great Again
          and secure a prosperous future for generations to come. As Trump often
          says, "The best is yet to come."
        </Paragraph>
        <Paragraph>
          Additional reflections highlight his enduring impact on American politics.
          His policies continue to spark debate and inspire new initiatives,
          adding further depth to his complex legacy.
        </Paragraph>
      </>
    ),
  },
  {
    id: "pw-news-2",
    title: "Exclusive Insights into the Future of AI",
    date: "January 10, 2025",
    paid: true, // Paid article
    image:
      "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Finsightscare.com%2Fwp-content%2Fuploads%2F2023%2F04%2FThe-Future-of-Artificial-Intelligence-Trends-and-Predictions.jpg&f=1&nofb=1&ipt=47fbcbb3dab97e72017a37e70525b23db8eebf4fd405cc7c7411b95e7807408f&ipo=images",
    content: (
      <>
        <Paragraph>
          Dive deep into the advancements in artificial intelligence and how
          they are poised to revolutionize various industries.
        </Paragraph>
        <Paragraph>
          Experts discuss the ethical implications and the potential for AI to
          improve human lives.
        </Paragraph>
        <Paragraph>
          This comprehensive analysis provides readers with a unique perspective
          on upcoming AI trends.
        </Paragraph>
        <Paragraph>
          In-depth reports indicate that AI innovations are accelerating rapidly.
          Cross-industry collaborations and diligent research are paving the way for transformative applications,
          reshaping the technological landscape significantly.
        </Paragraph>
        <Paragraph>
          Related news:{" "}
          <Link
            id={`related-article-link-pw-news-2-1`}
            aria-label={`Related article: AI and Healthcare Innovations`}
            to="pa-news-1"
          >
            AI and Healthcare Innovations
          </Link>,{" "}
          <Link
            id={`related-article-link-pw-news-2-2`}
            aria-label={`Related article: AI in Creative Industries`}
            to="pa-news-3"
          >
            AI in Creative Industries
          </Link>
        </Paragraph>
      </>
    ),
  },
  {
    id: "pw-news-3",
    title: "AI in Creative Industries: Transforming Art and Design",
    date: "February 15, 2025",
    paid: true, // Paid article
    image:
      "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimages.squarespace-cdn.com%2Fcontent%2Fv1%2F5ffc1ae692e37d47576a1330%2Ff83434fa-bef7-436b-ba9a-39c1f5b5ca66%2F6331b2d02d1a5651bd382688_CAI%2Bheader%2B01.jpg&f=1&nofb=1&ipt=ab9554cd42a7a28eb3a890c44d6a50c6413741c5534d485c826e11bd60039e51&ipo=images",
    content: (
      <>
        <Paragraph>
          Artificial intelligence is making significant inroads into the
          creative sectors, changing how art and design are created and
          consumed.
        </Paragraph>
        <Paragraph>
          This article explores the ways AI tools are being used by artists to
          enhance creativity and streamline the design process.
        </Paragraph>
        <Paragraph>
          It also delves into the debates surrounding the authenticity of
          AI-generated art and its impact on traditional artists.
        </Paragraph>
        <Paragraph>
          Related news:{" "}
          <Link
            id={`related-article-link-pw-news-3-1`}
            aria-label={`Related article: Exclusive Insights into the Future of AI`}
            to="pa-news-2"
          >
            Exclusive Insights into the Future of AI
          </Link>,{" "}
          <Link
            id={`related-article-link-pw-news-3-2`}
            aria-label={`Related article: The Role of AI in Modern Music Production`}
            to="pa-news-4"
          >
            The Role of AI in Modern Music Production
          </Link>
        </Paragraph>
      </>
    ),
  },
  {
    id: "pw-news-4",
    title: "The Role of AI in Modern Music Production",
    date: "March 20, 2025",
    paid: false, // Free article
    image:
      "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fres.cloudinary.com%2Felectronic-beats%2Fc_fit%2Cq_auto%2Cf_auto%2Cw_1920%2Fstage%2Fuploads%2F2018%2F02%2FAI_Electronic_Beats.png&f=1&nofb=1&ipt=02ad059af216e0a0cf1289d482ddcd9f0b4e121cc57dab0a1f68d6fea9f4986d&ipo=images",
    content: (
      <>
        <Paragraph>
          AI technologies are increasingly being integrated into music
          production, offering new tools and possibilities for artists and
          producers.
        </Paragraph>
        <Paragraph>
          This piece examines how AI is used in composing, mixing, and mastering
          music, and the benefits it brings to the creative process.
        </Paragraph>
        <Paragraph>
          It also addresses the challenges and ethical considerations of using
          AI in the music industry.
        </Paragraph>
        <Paragraph>
          Related news:{" "}
          <Link
            id={`related-article-link-pw-news-4-1`}
            aria-label={`Related article: AI in Creative Industries: Transforming Art and Design`}
            to="pa-news-3"
          >
            AI in Creative Industries: Transforming Art and Design
          </Link>,{" "}
          <Link
            id={`related-article-link-pw-news-4-2`}
            aria-label={`Related article: AI and the Future of Live Performances`}
            to="pa-news-5"
          >
            AI and the Future of Live Performances
          </Link>
        </Paragraph>
      </>
    ),
  },
  {
    id: "pw-news-5",
    title: "Crypto Market Surges Amid Regulatory Shifts",
    date: "April 20, 2025",
    paid: true, // Paid article
    image:
      "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.dunhamandcompany.com%2Fwp-content%2Fuploads%2F2020%2F05%2FGettyImages-1034363382-e1589830000885.jpg&f=1&nofb=1&ipt=81cf4579d9a6be1df89255d5fb1e6bfafa4a14051ca9f50feed64acc6262107a&ipo=images",
    content: (
      <>
        <Paragraph>
          The crypto market is experiencing a surge as new regulatory frameworks help stabilize investor confidence.
        </Paragraph>
        <Paragraph>
          Analysts note that clearer guidelines and institutional interest are propelling digital currencies into the mainstream.
        </Paragraph>
        <Paragraph>
          Related news:{" "}
          <Link
            id={`related-article-link-crypto-news-1-1`}
            aria-label={`Related article: Exclusive Insights into the Future of AI`}
            to="pw-news-2"
          >
            Exclusive Insights into the Future of AI
          </Link>
        </Paragraph>
      </>
    ),
  }
];

export default newsArticles;
