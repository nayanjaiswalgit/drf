from bs4 import BeautifulSoup
import json

# Example HTML content (use your actual HTML here)
html_content = '''<div class=""><div class="aHl"></div><div id=":np" tabindex="-1"></div><div id=":nf" class="ii gt" jslog="20277; u014N:xr6bB; 1:WyIjdGhyZWFkLWY6MTgxNzExODM2NDAxODk2NDEzNyJd; 4:WyIjbXNnLWY6MTgxNzExODM2NDAxODk2NDEzNyIsbnVsbCxudWxsLG51bGwsMCwwLFsxLDAsMF0sNTMsMzQ0LG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCwxLG51bGwsbnVsbCxbM10sbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsMF0."><div id=":ne" class="a3s aiL msg-5211518948607038318"><div class="adM">


















</div><div><div class="adM">
    </div><div id="m_-5211518948607038318notification" style="font-family:Amazon Ember;background-color:#ffffff;max-width:450px"><div class="adM">
    </div><table id="m_-5211518948607038318notificationTable" width="367px" style="border:1px solid #ccc;border-top:5px solid #f8981d;table-layout:fixed;max-width:450px">
        <tbody><tr>
            <td id="m_-5211518948607038318aPayLogo" style="background:#f4f4f5;height:58px;padding:0px 17px 0px 17px"> <div> <a href="https://nll1bq56.r.ap-south-1.awstrack.me/L0/https:%2F%2Fwww.amazon.in%2Fgp%2Fsva%2Fdashboard/1/010901937b385f7d-b7060ac8-0ae8-43a9-aaff-26d36887aff9-000000/mR8lHS6UiRPjUcEYegJ50vjzXl8=183" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://nll1bq56.r.ap-south-1.awstrack.me/L0/https:%252F%252Fwww.amazon.in%252Fgp%252Fsva%252Fdashboard/1/010901937b385f7d-b7060ac8-0ae8-43a9-aaff-26d36887aff9-000000/mR8lHS6UiRPjUcEYegJ50vjzXl8%3D183&amp;source=gmail&amp;ust=1733038012582000&amp;usg=AOvVaw2Vm149134xIpc6KETVuczp"><img src="https://ci3.googleusercontent.com/meips/ADKq_NZk73p8FlLkBNLMjRriAUqA17eakpf76HEiEMFUtmRb6SbhrSZRL00DaLYvUztJRjXzSY06j9i5zsU3Q_Hz1pEJUD7eOctVNH-74HR1REoSQQvP7j2F8O3KZX4Z_--zPQ6Jh64YXOCbCPUZ9Q=s0-d-e1-ft#https://m.media-amazon.com/images/G/31/Apay_Push_Automation/Tags/AmazonPay_Transparent" height="35" class="CToWUd" data-bit="iit"> </a>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td id="m_-5211518948607038318gapRow2" style="height:25px"></td>
                            </tr>
                <tr>
                    <td>
                        <table id="m_-5211518948607038318greetingMessage" width="360px" cellspacing="0" cellpadding="0" style="table-layout:fixed">
                        <tbody><tr>
                        <td id="m_-5211518948607038318greetings" style="margin:0px 0px 0px 0px;padding:0px 17px 0px 17px">Hi Maya,</td>
                        </tr>
                        <tr>
                            <td id="m_-5211518948607038318gapRow3" style="height:5px"></td>
                        </tr>
                        <tr>
                            <td id="m_-5211518948607038318messageText" style="margin:0px 0px 0px 0px;padding:0px 17px 0px 17px">Thanks for using Amazon Pay Wallet. Your payment was <b style="color:#008a00">successful</b>.</td>
                        </tr>
                        </tbody></table>
                    </td>
                </tr>
        <tr>
            <td id="m_-5211518948607038318gapRow3" style="height:20px"></td>
        </tr>
        <tr>
            <td>
                <table id="m_-5211518948607038318paymentHighlights" width="360px" cellspacing="0" cellpadding="0" style="table-layout:fixed;border-bottom:2px solid rgba(0,0,0,0.1)">
                    <tbody><tr>
                        <td id="m_-5211518948607038318paymentHighlightsHeading1" style="padding-left:17px">Paid to</td>
                        <td id="m_-5211518948607038318paymentHighlightsHeading2" style="padding-right:17px;text-align:right">Amount</td>
                    </tr>
                    <tr>
                        <td id="m_-5211518948607038318gapRow7" style="height:4px"></td>
                    </tr>
                    <tr>
                        <td id="m_-5211518948607038318bankName" style="padding-left:17px"><b>KHANGARAM</b></td>
                        <td id="m_-5211518948607038318amount" style="padding-right:17px;text-align:right"><b>₹10.00</b></td>
                    </tr>
                    <tr>
                        <td id="m_-5211518948607038318reportTransaction" style="padding-left:17px" colspan="2">To report any unauthorised transaction, please <a href="https://nll1bq56.r.ap-south-1.awstrack.me/L0/https:%2F%2Fwww.amazon.in%2Fcstxn/1/010901937b385f7d-b7060ac8-0ae8-43a9-aaff-26d36887aff9-000000/wABGcWSZqY8OtqrXMv0W7L2ivUw=183" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://nll1bq56.r.ap-south-1.awstrack.me/L0/https:%252F%252Fwww.amazon.in%252Fcstxn/1/010901937b385f7d-b7060ac8-0ae8-43a9-aaff-26d36887aff9-000000/wABGcWSZqY8OtqrXMv0W7L2ivUw%3D183&amp;source=gmail&amp;ust=1733038012582000&amp;usg=AOvVaw2YZq5ae9yZ3E-HhhkU4NvU">click here</a></td>
                    </tr>
                    </tbody></table>
            </td>
        </tr>
        <tr>
            <td id="m_-5211518948607038318gapRow4" style="height:20px"></td>
        </tr>
    <tr>
        <td>
            <table id="m_-5211518948607038318paymentDetails" width="326px" style="margin:0px 17px 0px 17px;table-layout:fixed">
            <tbody><tr>
                <td class="m_-5211518948607038318paymentDetailsHeading" width="50%">UPI Reference ID</td>
                <td class="m_-5211518948607038318paymentDetailsContent">433507759058</td>
            </tr>
            <tr>
                <td class="m_-5211518948607038318paymentDetailsHeading">Order Date</td>
                <td class="m_-5211518948607038318paymentDetailsContent">30 November 2024</td>
            </tr>
            </tbody></table>
        </td>
    </tr>
    <tr>
        <td id="m_-5211518948607038318gapRow4" style="height:25px"></td>
    </tr>
    <tr>
        <td id="m_-5211518948607038318summarytable" style="padding:0px 17px 0px 17px">
            <table id="m_-5211518948607038318tableBox" width="326px" style="table-layout:fixed;border:1px solid rgb(204,204,204)">
            <tbody><tr>
                <td id="m_-5211518948607038318tableTitleData1" style="width:50%;padding:10px;border-bottom:1px solid rgb(225,225,225)">Updated Amazon Pay Balance</td>
                <td id="m_-5211518948607038318tableTitleData2" style="padding:10px;text-align:right;border-bottom:1px solid rgb(225,225,225)">₹8532.38</td>
            </tr>
            <tr>
                <td id="m_-5211518948607038318tableData" style="padding:10px;text-align:left;color:rgb(17,17,17)">
                        Wallet</td>
                <td id="m_-5211518948607038318tableData" style="padding:10px;text-align:right">₹979.85</td>
            </tr>
            <tr>
                <td id="m_-5211518948607038318tableData" style="padding:10px;text-align:left">Gift Cards</td>
                <td id="m_-5211518948607038318tableData" style="padding:10px;text-align:right">₹7552.53</td>
            </tr>
        </tbody></table>
    </td>
    </tr>
    <tr>
        <td id="m_-5211518948607038318gapRow5" style="height:13px"></td>
    </tr>
    <tr>
        <td id="m_-5211518948607038318summarytable2" style="padding:0px 14px 0px 14px">
        <table id="m_-5211518948607038318redirectiveButtons" width="330px" style="table-layout:fixed">
                    <tbody><tr>
                        <td>
                            <div style="width:100%">
                                <a href="https://nll1bq56.r.ap-south-1.awstrack.me/L0/https:%2F%2Fwww.amazon.in%2Fgp%2Fpayment%2Fstatement/1/010901937b385f7d-b7060ac8-0ae8-43a9-aaff-26d36887aff9-000000/-ry5Fd55DPmSUng5OTv0ziOIGxU=183" style="text-align:center;text-decoration:none;color:inherit" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://nll1bq56.r.ap-south-1.awstrack.me/L0/https:%252F%252Fwww.amazon.in%252Fgp%252Fpayment%252Fstatement/1/010901937b385f7d-b7060ac8-0ae8-43a9-aaff-26d36887aff9-000000/-ry5Fd55DPmSUng5OTv0ziOIGxU%3D183&amp;source=gmail&amp;ust=1733038012582000&amp;usg=AOvVaw0CjSnGHpPHwq4wJTuyYFdM">
                                    <span id="m_-5211518948607038318button1">
                                        <span style="text-align:center;text-decoration:none;background:#f4d078;background:-webkit-linear-gradient(top,#f7dfa5,#f0c14b);background:linear-gradient(to bottom,#fcfcfd,#e6e9ec)">
                                            <span aria-hidden="true" style="background-color:#ffd852;border:0;display:block;font-size:18px;line-height:48px;margin:0;outline:0;text-align:center;white-space:nowrap;color:#111;text-decoration:none;font-weight:bold">
                                                View Statement
                                            </span>
                                        </span>
                                    </span>
                                </a>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td id="m_-5211518948607038318m_5778835476537988845gapRow13" style="height:3px"></td>
                    </tr>
                    <tr>
                        <td>
                            <div style="width:100%">
                                <a href="https://nll1bq56.r.ap-south-1.awstrack.me/L0/https:%2F%2Fwww.amazon.in%2Fgp%2Fsva%2Faddmoney/1/010901937b385f7d-b7060ac8-0ae8-43a9-aaff-26d36887aff9-000000/k02_azxjGvyuLDCsMq-mCGKM5tc=183" style="text-decoration:none;color:inherit;text-align:center;width:100%" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://nll1bq56.r.ap-south-1.awstrack.me/L0/https:%252F%252Fwww.amazon.in%252Fgp%252Fsva%252Faddmoney/1/010901937b385f7d-b7060ac8-0ae8-43a9-aaff-26d36887aff9-000000/k02_azxjGvyuLDCsMq-mCGKM5tc%3D183&amp;source=gmail&amp;ust=1733038012582000&amp;usg=AOvVaw16bQ36-LiDnqnsiQaM6tUz">
                                    <span id="m_-5211518948607038318button2">
                                        <span style="text-align:center;text-decoration:none;background:#e6e9ec;background:-webkit-linear-gradient(top,#f7dfa5,#f0c14b);background:linear-gradient(to bottom,#fcfcfd,#e6e9ec)">
                                            <span aria-hidden="true" style="background-color:#d6dae1;border:0;display:block;font-size:18px;line-height:48px;margin:0;outline:0;text-align:center;white-space:nowrap;color:#111;text-decoration:none;font-weight:bold">
                                                   Add Money
                                            </span>
                                        </span>
                                    </span>
                                </a>
                            </div>
                        </td>
                    </tr>
                </tbody></table>
        </td>
    </tr>
    <tr>
        <td id="m_-5211518948607038318gapRow5" style="height:15px"></td>
    </tr>
    <tr>
      <td id="m_-5211518948607038318banner" width="326px" style="padding:0px 17px 0px 17px">
        <div width="100%">
        <a href="https://nll1bq56.r.ap-south-1.awstrack.me/L0/https:%2F%2Fwww.amazon.in%2Fgp%2Fpwain%2Flanding%2Fb%2Fref_tag=apay_bal_scan_debit_emailer/1/010901937b385f7d-b7060ac8-0ae8-43a9-aaff-26d36887aff9-000000/jsQd2X_g9ZkhfHz0WClBwGfyym4=183" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://nll1bq56.r.ap-south-1.awstrack.me/L0/https:%252F%252Fwww.amazon.in%252Fgp%252Fpwain%252Flanding%252Fb%252Fref_tag%3Dapay_bal_scan_debit_emailer/1/010901937b385f7d-b7060ac8-0ae8-43a9-aaff-26d36887aff9-000000/jsQd2X_g9ZkhfHz0WClBwGfyym4%3D183&amp;source=gmail&amp;ust=1733038012582000&amp;usg=AOvVaw0fj1zzB04dZMWqTyFylT2v">
            <img src="https://ci3.googleusercontent.com/meips/ADKq_NYnJC343KiuFXheYy4wBekkTmqfszGkb_gLtDMFHoOCifGPyJ6m4dgIQ9CP4XGtNgHr50AxxZNrBMON2G7CWfW-NRPom1HsoZ9WgChUdbho6RnLMDubzA1UbaLlWldvNxcghMngSukfCw=s0-d-e1-ft#https://m.media-amazon.com/images/G/31/img19/AmazonPay/harshita/SVA/327x75_qr-2.jpg" style="border-radius:5px 5px 5px 5px" width="100%" class="CToWUd" data-bit="iit">
        </a>
        </div>
    </td>
    </tr>
    <tr>
        <td id="m_-5211518948607038318gapRow6" style="height:6px"></td>
    </tr>
    <tr>
        <td id="m_-5211518948607038318haloWidget" style="padding:0px 17px 0px 17px;text-align:center">
          <table style="table-layout:fixed;border:1px solid #cccccc;border-radius:5px 5px 5px 5px;width:100%" width="326px">
                    <tbody><tr><td style="vertical-align:middle">
                        <a href="http://nll1bq56.r.ap-south-1.awstrack.me/L0/www.amazon.in%2Fhfc%2FmobileRecharge%3Fref_=email_rewards_rech/1/010901937b385f7d-b7060ac8-0ae8-43a9-aaff-26d36887aff9-000000/RYTFBvG4tnaFzR-HwLS38mSFnZY=183" class="m_-5211518948607038318haloWidgetLink" target="_blank" data-saferedirecturl="https://www.google.com/url?q=http://nll1bq56.r.ap-south-1.awstrack.me/L0/www.amazon.in%252Fhfc%252FmobileRecharge%253Fref_%3Demail_rewards_rech/1/010901937b385f7d-b7060ac8-0ae8-43a9-aaff-26d36887aff9-000000/RYTFBvG4tnaFzR-HwLS38mSFnZY%3D183&amp;source=gmail&amp;ust=1733038012582000&amp;usg=AOvVaw0V5V2_ZQIz8p4fQ63Zs5BZ">
                            <img src="https://ci3.googleusercontent.com/meips/ADKq_NZ3ILoBiPupkcZqlgxa5tj64b5xErSyMPpdGXumaKF19WefCtE9XOGUfaQQPDWTXeHfpVSOCwqpgN4wybY0pFaI-LPc2qJ04K9p49ebE1W91swVXSawBRLuyfdmZghNW1iyfw=s0-d-e1-ft#https://m.media-amazon.com/images/G/31/AP4/Notifications/125X100-Recharge.jpg" width="69px" height="56px" class="CToWUd" data-bit="iit">
                        </a>
                    </td>
                    <td style="vertical-align:middle">
                        <a href="http://nll1bq56.r.ap-south-1.awstrack.me/L0/www.amazon.in%2Fhfc%2Fdth%3Fref_=email_rewards_dth/1/010901937b385f7d-b7060ac8-0ae8-43a9-aaff-26d36887aff9-000000/W0F33PLD6sY9ohbBUa0DiQ_aGTI=183" class="m_-5211518948607038318haloWidgetLink" target="_blank" data-saferedirecturl="https://www.google.com/url?q=http://nll1bq56.r.ap-south-1.awstrack.me/L0/www.amazon.in%252Fhfc%252Fdth%253Fref_%3Demail_rewards_dth/1/010901937b385f7d-b7060ac8-0ae8-43a9-aaff-26d36887aff9-000000/W0F33PLD6sY9ohbBUa0DiQ_aGTI%3D183&amp;source=gmail&amp;ust=1733038012582000&amp;usg=AOvVaw3ZmU2eof4hrf4Z8XNzLFd2">
                            <img src="https://ci3.googleusercontent.com/meips/ADKq_NZaZimEc3x0caplGsD65Hk10g26crNoqW7OxC3OQ4mKg2xDVSdEZN6kZ1eIAGEJSlt4d5xV64myOOV8lOmqRTME2oBtXXXtPTIz1ceSNMk7yvNyR_ftxpvSBC3PGC8=s0-d-e1-ft#https://m.media-amazon.com/images/G/31/AP4/Notifications/125X100_DTH.jpg" width="69px" height="56px" class="CToWUd" data-bit="iit">
                        </a>
                    </td>
                    <td style="vertical-align:middle">
                        <a href="http://nll1bq56.r.ap-south-1.awstrack.me/L0/www.amazon.in%2Fb%3Fnode=15246428031%26ref_=email_rewards_bill/1/010901937b385f7d-b7060ac8-0ae8-43a9-aaff-26d36887aff9-000000/7bOlSEoKKOwLt2HYIl269X93vPk=183" class="m_-5211518948607038318haloWidgetLink" target="_blank" data-saferedirecturl="https://www.google.com/url?q=http://nll1bq56.r.ap-south-1.awstrack.me/L0/www.amazon.in%252Fb%253Fnode%3D15246428031%2526ref_%3Demail_rewards_bill/1/010901937b385f7d-b7060ac8-0ae8-43a9-aaff-26d36887aff9-000000/7bOlSEoKKOwLt2HYIl269X93vPk%3D183&amp;source=gmail&amp;ust=1733038012582000&amp;usg=AOvVaw3RL29_Iy7aWpoigUaV2gMG">
                            <img src="https://ci3.googleusercontent.com/meips/ADKq_Nb1S3ZWiNTeAY2Jypre61ToSox1SVHsGCplzUpTtJFHMq-nfWnks4oWRz33HY908Lfjz8Ai4jn0EIf4OLBpO0pdYccjVfZLKIiFZfgaJAICozvDU8if2Khs0BVVusqSXwNHtw=s0-d-e1-ft#https://m.media-amazon.com/images/G/31/AP4/Notifications/125X100_PayBills.jpg" width="69px" height="56px" class="CToWUd" data-bit="iit">
                        </a>
                    </td>
                    <td style="vertical-align:middle">
                        <a href="http://nll1bq56.r.ap-south-1.awstrack.me/L0/www.amazon.in%2Fb%2F%3Fnode=21102071031%26ref_=email_rewards_oflp/1/010901937b385f7d-b7060ac8-0ae8-43a9-aaff-26d36887aff9-000000/rC3lEN3ADkKAp0vpT4Ah4Lrelqg=183" class="m_-5211518948607038318haloWidgetLink" target="_blank" data-saferedirecturl="https://www.google.com/url?q=http://nll1bq56.r.ap-south-1.awstrack.me/L0/www.amazon.in%252Fb%252F%253Fnode%3D21102071031%2526ref_%3Demail_rewards_oflp/1/010901937b385f7d-b7060ac8-0ae8-43a9-aaff-26d36887aff9-000000/rC3lEN3ADkKAp0vpT4Ah4Lrelqg%3D183&amp;source=gmail&amp;ust=1733038012582000&amp;usg=AOvVaw2zQAyL8cxmeF-QwY-nflYG">
                            <img src="https://ci3.googleusercontent.com/meips/ADKq_NYHZOjtZdDYPeeCF4hn3prYUCou6zhZjbHgacUmJyrPOdEMUWNJ_wk2-xcE_T5pu2R5k1ZlSVV0MQZc-rnwXpYQlZTNCO6UFN7gFk2dB05TgJAZX2ZO3HtpbgZ1kgoyV32u=s0-d-e1-ft#https://m.media-amazon.com/images/G/31/AP4/Notifications/125X100_Rewards.jpg" width="69px" height="56px" class="CToWUd" data-bit="iit">
                        </a>
                    </td>
                    <td style="vertical-align:middle">
                        <a href="http://nll1bq56.r.ap-south-1.awstrack.me/L0/www.amazon.in%2Famazonpay%2Fhome%3Fref_=email_rewards_dasp/1/010901937b385f7d-b7060ac8-0ae8-43a9-aaff-26d36887aff9-000000/NaEZ2TiOu2gD5y5e5B-E7DKUUPQ=183" class="m_-5211518948607038318haloWidgetLink" target="_blank" data-saferedirecturl="https://www.google.com/url?q=http://nll1bq56.r.ap-south-1.awstrack.me/L0/www.amazon.in%252Famazonpay%252Fhome%253Fref_%3Demail_rewards_dasp/1/010901937b385f7d-b7060ac8-0ae8-43a9-aaff-26d36887aff9-000000/NaEZ2TiOu2gD5y5e5B-E7DKUUPQ%3D183&amp;source=gmail&amp;ust=1733038012582000&amp;usg=AOvVaw0kw06zjhb0xuKJHHstJu6c">
                            <img src="https://ci3.googleusercontent.com/meips/ADKq_NYSnhEpfOCSM5EnmYdsC2Uaa4SrtWPcm3W-jpO9bppDdzrkugo4XjvbaE-AU1Tnw3C7YAPSR4Z6TgicUucT_vD7p-NHBznD-dk0alJnLrrBl6bheuV9ZHuWYYoDKMLb=s0-d-e1-ft#https://m.media-amazon.com/images/G/31/AP4/Notifications/125X100_More.jpg" width="69px" height="56px" class="CToWUd" data-bit="iit">
                        </a>
                    </td>
          </tr></tbody></table>
        </td>
    </tr>
      <tr>
        <td id="m_-5211518948607038318gapRow6" style="height:6px"></td>
      </tr>
      <tr>
        <td id="m_-5211518948607038318trustedAndSecurePayments" width="326px" style="padding:0px 15px 0px 15px;text-align:center">
          <table style="table-layout:fixed;width:100%">
            <tbody><tr>
              <td style="background-color:#f2f2f2;vertical-align:middle;text-align:center;height:44px;border-radius:5px 5px 5px 5px" width="326px">
                <img src="https://ci3.googleusercontent.com/meips/ADKq_NYPB6tvEE0KoJmKNdIrKmJcTl67j16k9SjWK-c4RnHmht4MNojQWa8k7GlsorDFdKLm6ByzCJqy5DjqsvEECE11ybLku8H8aDzDChugQ4CKDMDVAzRLdGLiZb89uVudaHwd5wTieC3M7bqYRn98Yw=s0-d-e1-ft#https://m.media-amazon.com/images/G/31/AP4/Notifications/TrustedAndSecurePaymentsIcon.png" style="text-align:center;display:inline-block;vertical-align:middle;padding-bottom:3px" height="35" width="35" class="CToWUd" data-bit="iit">
                    <font id="m_-5211518948607038318trustedAndSecurePaymentsText" style="vertical-align:middle;font-size:15px;line-height:18px">Trusted &amp; secure payments </font>
              </td>
            </tr>
          </tbody></table>

                </td>
              </tr>
        <tr>
        <td id="m_-5211518948607038318gapRow6" style="height:6px">
      </td></tr>
    </tbody></table>
			</div><img alt="" src="https://ci3.googleusercontent.com/meips/ADKq_NZWr6pJubVQPUQZIZWQ-PAGL_PUxUSudgyfpBgLIGd4s5D6CiOK55zlSRs1iFmWfQ-x1wohUHNtzfA0HjhufKlC32BxxrPfItCdm6NCS6hEUnw7TmrWafaZ8wRjMpjIxa3HOP8gIE7-Jzftfyu9vpsmtWiY6KPD_x5Rj8CjJFpPUryEML5x_PwNhG-ZCdBtAGRQe7YcHM-LJI_T6p8LSUc=s0-d-e1-ft#https://nll1bq56.r.ap-south-1.awstrack.me/I0/010901937b385f7d-b7060ac8-0ae8-43a9-aaff-26d36887aff9-000000/owOZ05wwt7zAqomh0DBY-Ns80m0=183" style="display:none;width:1px;height:1px" class="CToWUd" data-bit="iit"><div class="yj6qo"></div><div class="adL">
</div></div><div class="adL">
			
</div></div></div><div class="WhmR8e" data-hash="0"></div></div>
</div></div></div>
 '''


    # Parse the HTML content with BeautifulSoup
def parse_email(html):
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html, 'html5lib')
    
    # Get the plain text without any HTML tags
    text = soup.get_text()
    
    # Optionally, you can use .strip() to remove leading/trailing whitespaces
    cleaned_text = text.strip()
    
    return cleaned_text
    


import re
import json
import spacy

# Load the pre-trained spaCy model for English
nlp = spacy.load("en_core_web_sm")


def test() :
    # Parse the email HTML content
    parsed_data = parse_email(html_content)
    
    
  # Process the email content with spaCy
    doc = nlp(parsed_data)

    # Extract Named Entities
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Print extracted entities
    for entity in entities:
        print(f"Entity: {entity[0]}, Label: {entity[1]}")



    # Print the JSON result

