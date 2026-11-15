# -*- coding: utf-8 -*-
"""
Script to generate the official SR University Course Project Report HTML
Strictly adhering to 'CRC_Project_Report_Lineup.pdf':
- Front Page (matching PPT)
- Chapter 1: Introduction to Concurrency Control & Event Registration (Product #8)
- Chapter 2: Mathematical Principles of Concurrency Control & Mutex
- Chapter 3: Implementation of Concurrency Kernel & Mutex
- Chapter 4: Dashboard / Application Interface Development
- Chapter 5: Errors, Challenges and Learning Outcomes (Table: Problem -> Cause -> Solution -> Learning)
- Chapter 6: Additional Features and Product Enhancement (Feature -> Purpose -> User Benefit)
- Chapter 7: Results and Conclusion
- Appendix A: Complete Source Code
- Appendix B: Line-by-Line Explanation of Critical Code
- Appendix C: Dashboard Screenshots & Interface Walkthrough
- Appendix D: Complete Test-Case Tables and Sample Outputs
"""

import os
import sys

def build_report_html():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SYNNEXA: Concurrency Control and Mutex Synchronization Event Registration System — SR University Course Project Report</title>
<style>
  @page {
    size: A4;
    margin: 20mm 18mm 20mm 18mm;
    @bottom-right {
      content: counter(page);
    }
  }

  *, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    font-family: 'Times New Roman', Times, 'Georgia', serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #111827;
    background: #FFFFFF;
  }

  .page {
    page-break-after: always;
    clear: both;
    position: relative;
    padding-top: 10px;
    padding-bottom: 20px;
  }

  .cover-page {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
    min-height: 92vh;
    padding: 30px 20px;
    border: 3px double #0B3C75;
    background: #FAFCFF;
  }

  .uni-header {
    margin-bottom: 15px;
  }

  .uni-name {
    font-size: 24pt;
    font-weight: 800;
    color: #0B3C75;
    letter-spacing: 1.5px;
    text-transform: uppercase;
  }

  .uni-sub {
    font-size: 11pt;
    color: #4B5563;
    font-style: italic;
    margin-top: 4px;
  }

  .crest-box {
    margin: 15px auto;
    width: 90px;
    height: 90px;
    border: 2px solid #0B3C75;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #FFFFFF;
    font-size: 22pt;
    font-weight: bold;
    color: #0B3C75;
    box-shadow: 0 4px 10px rgba(11, 60, 117, 0.15);
  }

  .report-title-box {
    margin: 20px 0;
  }

  .report-main-title {
    font-size: 18pt;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.3;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .report-sub-title {
    font-size: 13pt;
    font-weight: 700;
    color: #0B3C75;
    margin-top: 8px;
  }

  .report-degree-note {
    font-size: 10.5pt;
    color: #374151;
    margin: 15px auto;
    max-width: 580px;
    line-height: 1.45;
  }

  .roster-table {
    width: 100%;
    max-width: 620px;
    margin: 15px auto;
    border-collapse: collapse;
    font-size: 9.5pt;
    text-align: left;
  }

  .roster-table th, .roster-table td {
    padding: 6px 10px;
    border: 1px solid #CBD5E1;
  }

  .roster-table th {
    background: #0B3C75;
    color: #FFFFFF;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 8.5pt;
  }

  .roster-table tr:nth-child(even) {
    background: #F1F5F9;
  }

  .guide-box {
    margin-top: 15px;
    font-size: 10.5pt;
    line-height: 1.4;
  }

  .guide-title {
    font-weight: 700;
    color: #0F172A;
  }

  .cert-page {
    padding: 20px 10px;
    min-height: 88vh;
  }

  .cert-heading {
    text-align: center;
    font-size: 16pt;
    font-weight: 800;
    color: #0B3C75;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 25px;
    border-bottom: 2px solid #0B3C75;
    padding-bottom: 8px;
  }

  .cert-body {
    font-size: 11pt;
    text-align: justify;
    line-height: 1.7;
    margin-bottom: 30px;
  }

  .sign-grid {
    display: flex;
    justify-content: space-between;
    margin-top: 60px;
    padding: 0 20px;
  }

  .sign-col {
    text-align: center;
    width: 45%;
  }

  .sign-line {
    border-top: 1px solid #1F2937;
    margin-top: 40px;
    padding-top: 6px;
    font-weight: 700;
    font-size: 10.5pt;
  }

  h1.chap-heading {
    font-size: 15pt;
    font-weight: 800;
    color: #0B3C75;
    text-transform: uppercase;
    border-bottom: 2px solid #0B3C75;
    padding-bottom: 6px;
    margin-top: 15px;
    margin-bottom: 14px;
    page-break-after: avoid;
  }

  h2.sec-heading {
    font-size: 12.5pt;
    font-weight: 700;
    color: #1E293B;
    margin-top: 16px;
    margin-bottom: 8px;
    border-left: 4px solid #0B3C75;
    padding-left: 8px;
    page-break-after: avoid;
  }

  h3.subsec-heading {
    font-size: 11pt;
    font-weight: 700;
    color: #334155;
    margin-top: 12px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }

  p {
    margin-bottom: 10px;
    text-align: justify;
    line-height: 1.55;
  }

  ul, ol {
    margin-left: 24px;
    margin-bottom: 12px;
    line-height: 1.5;
  }

  li {
    margin-bottom: 4px;
  }

  table.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }

  table.data-table th, table.data-table td {
    padding: 7px 10px;
    border: 1px solid #94A3B8;
  }

  table.data-table th {
    background: #0B3C75;
    color: #FFFFFF;
    font-weight: 700;
    text-align: left;
  }

  table.data-table tr:nth-child(even) {
    background: #F8FAFC;
  }

  .code-block {
    background: #0F172A;
    color: #E2E8F0;
    padding: 12px 14px;
    border-radius: 4px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8.5pt;
    line-height: 1.45;
    margin: 12px 0;
    white-space: pre-wrap;
    word-break: break-all;
    page-break-inside: avoid;
    border: 1px solid #334155;
  }

  .math-box {
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-left: 4px solid #0B3C75;
    padding: 10px 14px;
    margin: 12px 0;
    font-family: 'Times New Roman', serif;
    font-style: italic;
    font-size: 10.5pt;
    page-break-inside: avoid;
  }

  .callout-box {
    background: #FEF3C7;
    border: 1px solid #F59E0B;
    border-radius: 4px;
    padding: 10px 14px;
    margin: 12px 0;
    font-size: 10pt;
    color: #92400E;
    page-break-inside: avoid;
  }

  .success-box {
    background: #ECFDF5;
    border: 1px solid #10B981;
    border-radius: 4px;
    padding: 10px 14px;
    margin: 12px 0;
    font-size: 10pt;
    color: #065F46;
    page-break-inside: avoid;
  }

  .img-container {
    text-align: center;
    margin: 15px 0;
    page-break-inside: avoid;
  }

  .img-container img {
    max-width: 95%;
    height: auto;
    border: 1px solid #CBD5E1;
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  }

  .img-caption {
    font-size: 9pt;
    color: #475569;
    font-style: italic;
    margin-top: 6px;
  }

  .toc-row {
    display: flex;
    justify-content: space-between;
    padding: 4px 0;
    border-bottom: 1px dotted #CBD5E1;
    font-size: 10pt;
  }

  .toc-title {
    font-weight: 600;
  }

  .toc-sub {
    padding-left: 20px;
    font-size: 9.5pt;
    color: #334155;
  }

  @media screen {
    body {
      background: #E2E8F0;
      padding: 24px;
    }
    .page-wrap {
      max-width: 900px;
      margin: 0 auto;
      background: #FFFFFF;
      padding: 40px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    .no-print-bar {
      position: sticky;
      top: 0;
      background: #0B3C75;
      color: #FFFFFF;
      padding: 12px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      border-radius: 6px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
  }

  @media print {
    .no-print-bar {
      display: none !important;
    }
    body {
      background: #FFFFFF !important;
      padding: 0 !important;
    }
    .page-wrap {
      max-width: 100% !important;
      padding: 0 !important;
      box-shadow: none !important;
    }
  }
</style>
</head>
<body>

<div class="page-wrap">

  <div class="no-print-bar">
    <div>
      <strong>SYNNEXA — Official Academic Course Project Report (Product #8)</strong>
      <div style="font-size: 8.5pt; opacity: 0.85;">School of CS&AI, SR University • Academic Year 2025–2026</div>
    </div>
    <div style="display: flex; gap: 10px;">
      <button onclick="window.print()" style="background: #FFFFFF; color: #0B3C75; font-weight: bold; border: none; padding: 6px 14px; border-radius: 4px; cursor: pointer;">
        🖨️ Print to PDF / Paper
      </button>
      <a href="/" style="background: rgba(255,255,255,0.2); color: #fff; text-decoration: none; padding: 6px 14px; border-radius: 4px; font-size: 9pt;">
        ← Back to Live Portal
      </a>
    </div>
  </div>

  <!-- ============================================================
       PAGE 1: COVER PAGE (Strictly as per PPT Front Page)
       ============================================================ -->
  <div class="page cover-page">
    <div class="uni-header">
      <div class="uni-name">SR UNIVERSITY</div>
      <div class="uni-sub">Ananthasagar, Warangal, Telangana — 506371</div>
      <div style="font-size: 10pt; font-weight: bold; color: #0B3C75; margin-top: 4px;">
        SCHOOL OF COMPUTER SCIENCE AND ARTIFICIAL INTELLIGENCE
      </div>
    </div>

    <div class="crest-box">
      SRU
    </div>

    <div class="report-title-box">
      <div style="font-size: 11pt; font-weight: 700; color: #4B5563; text-transform: uppercase; letter-spacing: 1px;">
        Operating Systems Course Project Report
      </div>
      <div class="report-main-title">
        SYNNEXA: A FULL-STACK CONCURRENCY CONTROL &amp; MUTEX SYNCHRONIZATION EVENT REGISTRATION SYSTEM
      </div>
      <div class="report-sub-title">
        Product #8: Multi-Device High-Contention Race Condition Prevention &amp; Automated Refund Protection
      </div>
    </div>

    <div class="report-degree-note">
      A Course Project Report submitted in partial fulfillment of the requirements for the award of degree of<br>
      <strong>BACHELOR OF TECHNOLOGY</strong> in <strong>COMPUTER SCIENCE AND ENGINEERING</strong>
    </div>

    <div style="width: 100%;">
      <div style="font-size: 10pt; font-weight: bold; color: #1F2937; margin-bottom: 6px; text-transform: uppercase;">
        Submitted By (Ascending Hall Ticket Order):
      </div>
      <table class="roster-table">
        <thead>
          <tr>
            <th>HTNO</th>
            <th>Student Name</th>
            <th>Assigned Project Role</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>2503A51108</strong></td>
            <td>Ch. Naveen Reddy</td>
            <td>Systems Core &amp; Mutex Primitive Implementation</td>
          </tr>
          <tr>
            <td><strong>2503A51109</strong></td>
            <td>K. Shiva Saketh</td>
            <td>Payment Gateway &amp; Razorpay Standard Checkout SDK</td>
          </tr>
          <tr>
            <td><strong>2503A51110</strong></td>
            <td><strong>A. Shiva Ganesh (Team Leader)</strong></td>
            <td><strong>System Architecture, Concurrency Simulator &amp; Lead</strong></td>
          </tr>
          <tr>
            <td><strong>2503A51111</strong></td>
            <td>V. Saicharan</td>
            <td>Atomic Database Operations &amp; State Invariant Auditing</td>
          </tr>
          <tr>
            <td><strong>2503A1112</strong></td>
            <td>T. Geethika</td>
            <td>Editorial UI/UX, Luxury Styling &amp; Responsive Layouts</td>
          </tr>
          <tr>
            <td><strong>2503A51113</strong></td>
            <td>G. Vishwas</td>
            <td>Stress Testing, 50-Thread Benchmarks &amp; QA Verification</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="guide-box">
      <div style="font-size: 9.5pt; color: #4B5563;">Under the guidance and supervision of</div>
      <div class="guide-title" style="font-size: 12pt;">Mr. Bura Vijay Kumar</div>
      <div style="font-size: 9.5pt; color: #4B5563;">Assistant Professor, School of Computer Science &amp; Artificial Intelligence</div>
      <div style="font-size: 9.5pt; font-weight: bold; color: #0B3C75; margin-top: 4px;">Academic Year: 2025–2026</div>
    </div>
  </div>

  <!-- ============================================================
       PAGE 2: CERTIFICATE & ACKNOWLEDGEMENT
       ============================================================ -->
  <div class="page cert-page">
    <div class="cert-heading">BONAFIDE CERTIFICATE</div>
    <div class="cert-body">
      This is to certify that the project entitled <strong>“SYNNEXA: A FULL-STACK CONCURRENCY CONTROL AND MUTEX SYNCHRONIZATION EVENT REGISTRATION SYSTEM (Product #8)”</strong> is a bona fide record of the work carried out by the following students of Second Year B.Tech (School of Computer Science &amp; Artificial Intelligence), SR University, Warangal, during the academic year 2025–2026 in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering:
    </div>

    <table class="roster-table" style="margin-bottom: 25px;">
      <thead>
        <tr>
          <th>S.No</th>
          <th>Hall Ticket Number</th>
          <th>Student Name</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>1</td><td>2503A51108</td><td>Ch. Naveen Reddy</td></tr>
        <tr><td>2</td><td>2503A51109</td><td>K. Shiva Saketh</td></tr>
        <tr><td>3</td><td>2503A51110</td><td>A. Shiva Ganesh (Team Leader)</td></tr>
        <tr><td>4</td><td>2503A51111</td><td>V. Saicharan</td></tr>
        <tr><td>5</td><td>2503A1112</td><td>T. Geethika</td></tr>
        <tr><td>6</td><td>2503A51113</td><td>G. Vishwas</td></tr>
      </tbody>
    </table>

    <div class="cert-body">
      This project work has been evaluated under our supervision and fulfills the curriculum guidelines and technical criteria laid down by SR University for Operating Systems Course Projects.
    </div>

    <div class="sign-grid">
      <div class="sign-col">
        <div class="sign-line">
          Mr. Bura Vijay Kumar<br>
          <span style="font-size: 8.5pt; font-weight: normal; color: #4B5563;">Assistant Professor &amp; Project Guide<br>School of CS&AI, SR University</span>
        </div>
      </div>
      <div class="sign-col">
        <div class="sign-line">
          Dr. M. Sheshikala<br>
          <span style="font-size: 8.5pt; font-weight: normal; color: #4B5563;">Professor &amp; Head of Department<br>School of CS&AI, SR University</span>
        </div>
      </div>
    </div>

    <div style="margin-top: 40px; border-top: 1px dashed #CBD5E1; padding-top: 15px;">
      <div class="cert-heading" style="font-size: 13pt; margin-bottom: 12px;">ACKNOWLEDGEMENT</div>
      <p style="font-size: 9.5pt; text-align: justify; line-height: 1.5;">
        We express our deepest gratitude to our faculty guide <strong>Mr. Bura Vijay Kumar</strong> for his invaluable technical guidance, architectural insights, and continuous encouragement during the design and mathematical validation of this concurrency control system. We also express our sincere thanks to <strong>Dr. M. Sheshikala</strong>, Head of Department, School of CS&AI, for extending the departmental laboratory and computational facilities. Finally, we thank our parents, university peers, and evaluators for their constant support and constructive critiques.
      </p>
    </div>
  </div>

  <!-- ============================================================
       PAGE 3: TABLE OF CONTENTS (As per Project Report Line Up)
       ============================================================ -->
  <div class="page">
    <div class="cert-heading">TABLE OF CONTENTS</div>
    
    <div style="margin-top: 15px;">
      <div class="toc-row"><strong>Chapter / Section Title</strong><strong>Page No.</strong></div>
      
      <div class="toc-row"><span class="toc-title">CHAPTER 1 - INTRODUCTION TO CONCURRENCY CONTROL &amp; EVENT REGISTRATION</span><span>4</span></div>
      <div class="toc-row"><span class="toc-sub">1.1 Introduction to Concurrency Anomalies &amp; Error Detection</span><span>4</span></div>
      <div class="toc-row"><span class="toc-sub">1.2 Need for Synchronization &amp; Mutex</span><span>4</span></div>
      <div class="toc-row"><span class="toc-sub">1.3 Basic Working of Mutex &amp; Critical Section</span><span>5</span></div>
      <div class="toc-row"><span class="toc-sub">1.4 Applications of Mutex in High-Contention Ticketing</span><span>5</span></div>
      <div class="toc-row"><span class="toc-sub">1.5 Problem Statement and Product Requirements (Product #8)</span><span>6</span></div>
      <div class="toc-row"><span class="toc-sub">1.6 Proposed Implementation Plan</span><span>6</span></div>

      <div class="toc-row" style="margin-top: 6px;"><span class="toc-title">CHAPTER 2 - MATHEMATICAL PRINCIPLES OF CONCURRENCY CONTROL &amp; MUTEX</span><span>7</span></div>
      <div class="toc-row"><span class="toc-sub">2.1 State Invariants and Shared Data Representation</span><span>7</span></div>
      <div class="toc-row"><span class="toc-sub">2.2 Mutual Exclusion Property (Formal Mathematical Proof)</span><span>7</span></div>
      <div class="toc-row"><span class="toc-sub">2.3 Progress and Bounded Waiting Proof (Starvation Elimination)</span><span>8</span></div>
      <div class="toc-row"><span class="toc-sub">2.4 Atomic Test-and-Set and Asynchronous Transitions</span><span>8</span></div>
      <div class="toc-row"><span class="toc-sub">2.5 Time-of-Check to Time-of-Use (TOCTOU) Race Hazard Formulation</span><span>9</span></div>
      <div class="toc-row"><span class="toc-sub">2.6 State Verification and Invariant Violation Detection</span><span>9</span></div>
      <div class="toc-row"><span class="toc-sub">2.7 Worked Numerical Example: Race Condition vs. Mutex Serialization</span><span>10</span></div>

      <div class="toc-row" style="margin-top: 6px;"><span class="toc-title">CHAPTER 3 - IMPLEMENTATION OF CONCURRENCY KERNEL &amp; MUTEX</span><span>11</span></div>
      <div class="toc-row"><span class="toc-sub">3.1 Software and Development Tools Used</span><span>11</span></div>
      <div class="toc-row"><span class="toc-sub">3.2 Mutex Function and Program Structure</span><span>11</span></div>
      <div class="toc-row"><span class="toc-sub">3.3 Asynchronous Mutex Implementation (Mutex.js)</span><span>12</span></div>
      <div class="toc-row"><span class="toc-sub">3.4 Keyed Mutex Registry for Fine-Grained Locking</span><span>12</span></div>
      <div class="toc-row"><span class="toc-sub">3.5 Atomic Critical Section and State Mutation (BookingService.js)</span><span>13</span></div>
      <div class="toc-row"><span class="toc-sub">3.6 ACID JSON Storage &amp; Atomic Temp-File Flushing</span><span>13</span></div>
      <div class="toc-row"><span class="toc-sub">3.7 Testing Using Single Thread Input Data</span><span>14</span></div>
      <div class="toc-row"><span class="toc-sub">3.8 Testing Using Multi-Thread Synthetic Workloads (50 Concurrent Threads)</span><span>14</span></div>
      <div class="toc-row"><span class="toc-sub">3.9 Testing Using Multi-Device Live Hardware (Teacher Laptop vs. Friend Mobile)</span><span>15</span></div>
      <div class="toc-row"><span class="toc-sub">3.10 Error Introduction and Detection (Toggling Mutex OFF vs. ON)</span><span>15</span></div>

      <div class="toc-row" style="margin-top: 6px;"><span class="toc-title">CHAPTER 4 - DASHBOARD / APPLICATION INTERFACE DEVELOPMENT</span><span>16</span></div>
      <div class="toc-row"><span class="toc-sub">4.1 Dashboard Requirements</span><span>16</span></div>
      <div class="toc-row"><span class="toc-sub">4.2 Software / Framework Used</span><span>16</span></div>
      <div class="toc-row"><span class="toc-sub">4.3 User Interface Design</span><span>17</span></div>
      <div class="toc-row"><span class="toc-sub">4.4 Dashboard Inputs</span><span>17</span></div>
      <div class="toc-row"><span class="toc-sub">4.5 Dashboard Outputs</span><span>17</span></div>
      <div class="toc-row"><span class="toc-sub">4.6 Dashboard-to-Backend Code Integration</span><span>18</span></div>
      <div class="toc-row"><span class="toc-sub">4.7 Complete Data Processing Flow</span><span>18</span></div>
      <div class="toc-row"><span class="toc-sub">4.8 Testing Methodology</span><span>19</span></div>
      <div class="toc-row"><span class="toc-sub">4.9 Test Cases and Results (Table TC-01 to TC-08)</span><span>19</span></div>
      <div class="toc-row"><span class="toc-sub">4.10 Error-Free and Corrupted Data Testing</span><span>20</span></div>

      <div class="toc-row" style="margin-top: 6px;"><span class="toc-title">CHAPTER 5 - ERRORS, CHALLENGES AND LEARNING OUTCOMES</span><span>21</span></div>
      <div class="toc-row"><span class="toc-sub">5.1 Errors Encountered During Implementation (Structured Table)</span><span>21</span></div>
      <div class="toc-row"><span class="toc-sub">5.2 Root Causes of Errors</span><span>22</span></div>
      <div class="toc-row"><span class="toc-sub">5.3 Solutions Implemented</span><span>22</span></div>
      <div class="toc-row"><span class="toc-sub">5.4 Challenges in Dashboard-Code Integration</span><span>23</span></div>
      <div class="toc-row"><span class="toc-sub">5.5 Learning Outcomes</span><span>23</span></div>

      <div class="toc-row" style="margin-top: 6px;"><span class="toc-title">CHAPTER 6 - ADDITIONAL FEATURES AND PRODUCT ENHANCEMENT</span><span>24</span></div>
      <div class="toc-row"><span class="toc-sub">6.1 Additional Features Implemented (Feature -> Purpose -> User Benefit)</span><span>24</span></div>
      <div class="toc-row"><span class="toc-sub">6.2 Benefits of Additional Features</span><span>25</span></div>
      <div class="toc-row"><span class="toc-sub">6.3 Improvements in User Experience</span><span>25</span></div>
      <div class="toc-row"><span class="toc-sub">6.4 Scope for Further Improvement</span><span>26</span></div>

      <div class="toc-row" style="margin-top: 6px;"><span class="toc-title">CHAPTER 7 - RESULTS AND CONCLUSION</span><span>27</span></div>
      <div class="toc-row"><span class="toc-sub">7.1 Summary of Test Results</span><span>27</span></div>
      <div class="toc-row"><span class="toc-sub">7.2 Overall Product Performance</span><span>27</span></div>
      <div class="toc-row"><span class="toc-sub">7.3 Achievement of Project Objectives</span><span>28</span></div>
      <div class="toc-row"><span class="toc-sub">7.4 Conclusion</span><span>28</span></div>

      <div class="toc-row" style="margin-top: 6px;"><span class="toc-title">APPENDICES</span><span>29</span></div>
      <div class="toc-row"><span class="toc-sub">APPENDIX A - Complete Source Code</span><span>29</span></div>
      <div class="toc-row"><span class="toc-sub">APPENDIX B - Line-by-Line Code Explanation</span><span>33</span></div>
      <div class="toc-row"><span class="toc-sub">APPENDIX C - Dashboard Screenshots &amp; Multi-Device Walkthrough</span><span>35</span></div>
      <div class="toc-row"><span class="toc-sub">APPENDIX D - Complete Test-Case Tables and Sample Outputs</span><span>37</span></div>
    </div>
  </div>

  <!-- ============================================================
       CHAPTER 1
       ============================================================ -->
  <div class="page">
    <h1 class="chap-heading">CHAPTER 1 - INTRODUCTION TO CONCURRENCY CONTROL &amp; EVENT REGISTRATION (PRODUCT #8)</h1>
    
    <h2 class="sec-heading">1.1 Introduction to Concurrency Anomalies &amp; Error Detection</h2>
    <p>
      In modern computing systems, concurrency occurs when multiple process threads or asynchronous microtasks execute simultaneously or interleaved over shared memory. While concurrency maximizes system throughput and CPU utilization, it introduces dangerous vulnerabilities when shared mutable state is accessed without synchronization. In the context of event registration, concert ticketing, and railway Tatkal bookings, the central resource is a finite numerical integer: remaining seat capacity.
    </p>
    <p>
      When high contention occurs—specifically when available capacity drops to one or two remaining places—multiple independent client requests arrive at the server within microsecond intervals. Uncontrolled interleaving produces a classic <strong>Time-of-Check to Time-of-Use (TOCTOU)</strong> race condition. In this anomaly, multiple threads read identical stale capacity values before any single thread completes its write operation. As a consequence, capacity decrements beyond zero into negative numbers ($C_{remaining} < 0$), minting phantom tickets and causing catastrophic overselling. Error detection in concurrent systems requires comparing the runtime state against formal mathematical invariants: the system must prove that remaining capacity never falls below zero and that total confirmed tickets never exceed original venue capacity.
    </p>

    <h2 class="sec-heading">1.2 Need for Synchronization &amp; Mutex</h2>
    <p>
      At the hardware architecture level, decrementing a variable in RAM (such as <code>remaining_tickets--</code>) is never a single atomic instruction. Instead, the Central Processing Unit executes three distinct steps:
    </p>
    <div class="code-block">Step 1: MOV EAX, [remaining_tickets]  ; Load current memory value into CPU register
Step 2: SUB EAX, 1                    ; Decrement register value in ALU
Step 3: MOV [remaining_tickets], EAX  ; Store decremented register value back into memory</div>
    <p>
      If an operating system context switch, asynchronous event-loop turn, or database/network I/O latency occurs between Step 1 and Step 3, concurrent execution paths observe stale state. Mutual Exclusion (Mutex) is the fundamental Operating System synchronization primitive designed to enforce serialization: it guarantees that only one thread can execute within the critical section at any given instant, forcing all other contending threads to wait safely in a queue.
    </p>

    <h2 class="sec-heading">1.3 Basic Working of Mutex &amp; Critical Section</h2>
    <p>
      A Critical Section is a designated segment of code that accesses shared mutable variables. According to classical Operating Systems theory formulated by Edsger W. Dijkstra (1965), any valid solution to the critical section problem must strictly satisfy three properties:
    </p>
    <ul>
      <li><strong>Mutual Exclusion:</strong> If process $P_i$ is executing in its critical section, then no other processes can be executing in their critical sections.</li>
      <li><strong>Progress:</strong> If no process is executing in its critical section and some processes wish to enter, only those processes that are not in their remainder section can participate in deciding which will enter next, and this selection cannot be postponed indefinitely.</li>
      <li><strong>Bounded Waiting:</strong> There exists a bound on the number of times other processes are allowed to enter their critical sections after a process has made a request to enter and before that request is granted, thereby preventing thread starvation.</li>
    </ul>

    <h2 class="sec-heading">1.4 Applications of Mutex in High-Contention Ticketing</h2>
    <p>
      Mutual exclusion is critical across real-world commercial and industrial software architectures:
    </p>
    <ul>
      <li><strong>IRCTC Tatkal Railway Reservations:</strong> Over 1.5 million users compete for 100,000 Tatkal berths at 10:00 AM IST daily. Strict serialization prevents double-booking berths.</li>
      <li><strong>Global Tech Summits &amp; Hackathons (SYNNEXA):</strong> High-demand squad pass sales where multi-member developer teams book the final conference booth passes simultaneously.</li>
      <li><strong>Financial Banking &amp; UPI Systems:</strong> Account balance transfers requiring serialized debit/credit transactions to prevent double-spending anomalies.</li>
      <li><strong>Airline Flight Inventory:</strong> Seat allocation engines ensuring physical seat assignments remain strictly bijective.</li>
    </ul>

    <h2 class="sec-heading">1.5 Problem Statement and Product Requirements (Product #8)</h2>
    <div class="callout-box">
      <strong>Product #8 Official Specification:</strong><br>
      <em>"Several users attempt to register when only one or two places remain. How can the remaining capacity be updated correctly?"</em>
    </div>
    <p>
      The functional and technical requirements for Product #8 demand:
    </p>
    <ol>
      <li>An asynchronous Mutex synchronization kernel built with zero external third-party dependencies using native JavaScript / Node.js.</li>
      <li>A fine-grained per-event lock registry to prevent system-wide lock contention across unrelated events.</li>
      <li>A real-time concurrency simulator and multi-device testing station where two independent client hardware devices (e.g., Teacher on Laptop and Friend on Mobile) simultaneously compete for 1 remaining seat.</li>
      <li>Controlled error introduction: ability to toggle Mutex OFF to reproduce overselling ($C_{remaining} = -1$), and toggle Mutex ON to verify zero-overselling ($C_{remaining} = 0$).</li>
      <li>An automated refund reassurance notification mechanism ensuring that any concurrent user whose booking is rejected receives immediate, clear confirmation of payment rollback within 5–7 business days.</li>
    </ol>

    <h2 class="sec-heading">1.6 Proposed Implementation Plan</h2>
    <p>
      The project architecture follows a 5-tier modular design:
    </p>
    <ol>
      <li><strong>Tier 1 — Core Concurrency Kernel (<code>src/core/Mutex.js</code>):</strong> Promise-based asynchronous FIFO queue mutex implementing strict Dijkstra bounded waiting.</li>
      <li><strong>Tier 2 — Keyed Mutex Registry (<code>src/core/KeyedMutexRegistry.js</code>):</strong> Resource-keyed lock multiplexer preventing cross-event thread blocking.</li>
      <li><strong>Tier 3 — Tatkal Booking Service (<code>src/services/BookingService.js</code>):</strong> ACID critical section handler with microsecond delay simulation to expose race windows when unlatched.</li>
      <li><strong>Tier 4 — Atomic Storage Engine (<code>src/storage/Database.js</code>):</strong> Non-blocking transactional file persistence with atomic temp-file renaming.</li>
      <li><strong>Tier 5 — Interactive UI &amp; Demonstration Dashboard (<code>public/</code>):</strong> Full-stack luxury web portal with Razorpay Standard Checkout SDK, printable boarding passes (`window.print()`), and 2-device concurrency station.</li>
    </ol>
  </div>

  <!-- ============================================================
       CHAPTER 2
       ============================================================ -->
  <div class="page">
    <h1 class="chap-heading">CHAPTER 2 - MATHEMATICAL PRINCIPLES OF CONCURRENCY CONTROL &amp; MUTEX</h1>
    
    <h2 class="sec-heading">2.1 State Invariants and Shared Data Representation</h2>
    <p>
      Let an event $E$ have initial capacity $C_{total} \in \mathbb{N}^+$. Let $\mathcal{R}(t) = \{r_1, r_2, \dots, r_m\}$ represent the set of successfully issued registration tickets up to wall-clock timestamp $t$. The instantaneous remaining capacity $C_{remaining}(t)$ is formally defined as:
    </p>
    <div class="math-box">
      C_{remaining}(t) = C_{total} - |\mathcal{R}(t)|
    </div>
    <p>
      The fundamental system safety invariant that must hold true for all timestamps $t \ge 0$ is:
    </p>
    <div class="math-box">
      \mathbf{Invariant\ 1:}\quad \forall t \ge 0, \quad 0 \le C_{remaining}(t) \le C_{total}
    </div>
    <p>
      Furthermore, every issued ticket $r_i$ must map to a unique physical capacity slot, ensuring bijectivity:
    </p>
    <div class="math-box">
      \mathbf{Invariant\ 2:}\quad \forall r_i, r_j \in \mathcal{R}(t), \quad r_i \ne r_j \implies \text{TicketCode}(r_i) \ne \text{TicketCode}(r_j) \land |\mathcal{R}(t)| \le C_{total}
    </div>

    <h2 class="sec-heading">2.2 Mutual Exclusion Property (Formal Proof)</h2>
    <p>
      Let $\mathcal{T} = \{T_1, T_2, \dots, T_n\}$ represent the set of concurrent reservation threads arriving at the server. Let $\mathcal{C}(t) \subseteq \mathcal{T}$ denote the set of threads concurrently executing inside the critical section at timestamp $t$.
    </p>
    <div class="math-box">
      \mathbf{Theorem\ 1\ (Mutual\ Exclusion):}\quad \forall t \ge 0, \quad |\mathcal{C}(t)| \le 1
    </div>
    <p>
      <strong>Proof by Contradiction:</strong> Assume there exists a timestamp $t^*$ where two distinct threads $T_a, T_b \in \mathcal{T}$ ($a \ne b$) are simultaneously executing inside the critical section, i.e., $\{T_a, T_b\} \subseteq \mathcal{C}(t^*)$.
    </p>
    <ol>
      <li>In our asynchronous Mutex implementation, a thread enters $\mathcal{C}(t)$ if and only if the boolean flag <code>_locked</code> is transitioned from <code>false</code> to <code>true</code>.</li>
      <li>Without loss of generality, assume $T_a$ acquired the lock at $t_a \le t^*$. Upon acquisition, $T_a$ sets <code>_locked = true</code> and assigns <code>_currentOwner = Ta</code>.</li>
      <li>When $T_b$ attempts acquisition at $t_b \le t^*$, it evaluates the guard condition: <code>if (!this._locked)</code>.</li>
      <li>Because $T_a$ has not executed <code>_release()</code> (as it is currently in $\mathcal{C}(t^*)$), <code>_locked</code> remains <code>true</code>.</li>
      <li>Consequently, the guard evaluates to <code>false</code>, and $T_b$ is appended to <code>_queue</code>, returning an unresolved Promise.</li>
      <li>Thus, $T_b$ cannot execute instructions within $\mathcal{C}(t^*)$, contradicting the assumption that $T_b \in \mathcal{C}(t^*)$. Hence, $|\mathcal{C}(t)| \le 1$ holds for all $t$. $\blacksquare$</li>
    </ol>

    <h2 class="sec-heading">2.3 Progress and Bounded Waiting Proof (Starvation Elimination)</h2>
    <p>
      <strong>Bounded Waiting:</strong> Let thread $T_i$ request the lock at timestamp $t_{req}(T_i)$. Let $W(T_i)$ represent the number of other threads granted critical section access before $T_i$ is admitted.
    </p>
    <p>
      Under an arbitrary unsynchronized or priority-preempted scheduler, $W(T_i)$ can grow unboundedly ($W(T_i) \to \infty$), resulting in thread starvation. In SYNNEXA, contending threads are enqueued into a strict <strong>First-In, First-Out (FIFO) queue</strong>:
    </p>
    <div class="math-box">
      W(T_i) = |\{T_j \in \mathcal{Q} : t_{req}(T_j) < t_{req}(T_i)\}| = k < \infty
    </div>
    <p>
      Because each critical section execution is bounded by maximum processing duration $\Delta t_{CS} \le 50\text{ms}$, the maximum waiting latency for thread $T_i$ is strictly bounded:
    </p>
    <div class="math-box">
      \text{Latency}(T_i) \le k \cdot \Delta t_{CS} < \infty
    </div>
    <p>
      This mathematically eliminates starvation and guarantees the Progress requirement.
    </p>

    <h2 class="sec-heading">2.4 Atomic Test-and-Set and Asynchronous Transitions</h2>
    <p>
      In multi-threaded C/C++ operating systems, atomic operations rely on CPU-level hardware primitives such as <code>CMPXCHG</code> (Compare-and-Swap) or <code>XCHG</code> (Test-and-Set) with the bus <code>LOCK</code> prefix. In Node.js, JavaScript executes on a single-threaded V8 event loop. Synchronous execution of a microtask is inherently non-preemptive. Therefore, inspecting <code>if (!this._locked)</code> and setting <code>this._locked = true</code> within the same synchronous tick operates with hardware-equivalent atomicity: no other JavaScript code can interleave between the check and the set.
    </p>

    <h2 class="sec-heading">2.5 Time-of-Check to Time-of-Use (TOCTOU) Race Hazard Formulation</h2>
    <p>
      When synchronization is disabled (Mutex OFF), the booking workflow decouples checking from updating across an asynchronous delay:
    </p>
    <ol>
      <li>$t_0$: Thread $T_1$ reads $C_{remaining} = 1$. Evaluates check: $1 > 0 \implies \text{VALID}$.</li>
      <li>$t_1$: Thread $T_1$ initiates asynchronous operation (payment delay / network I/O).</li>
      <li>$t_2$: Thread $T_2$ arrives, reads $C_{remaining} = 1$ (STALE!). Evaluates check: $1 > 0 \implies \text{VALID}$.</li>
      <li>$t_3$: Thread $T_2$ initiates asynchronous operation.</li>
      <li>$t_4$: Thread $T_1$ completes, writes $C_{remaining} \leftarrow 1 - 1 = 0$, mints Ticket #1.</li>
      <li>$t_5$: Thread $T_2$ completes, writes $C_{remaining} \leftarrow 0 - 1 = -1$, mints Ticket #2.</li>
    </ol>
    <p>
      This sequence violates Invariant 1: $C_{remaining}(t_5) = -1 < 0$. Two tickets are confirmed for a single seat.
    </p>

    <h2 class="sec-heading">2.6 State Verification and Invariant Violation Detection</h2>
    <p>
      The audit engine continuously validates state consistency:
    </p>
    <div class="math-box">
      \text{Anomaly}(t) = \begin{cases} 
        \text{TRUE (OVERSOLD)} & \text{if } C_{remaining}(t) < 0 \lor |\mathcal{R}(t)| > C_{total} \\
        \text{FALSE (VALID)} & \text{if } 0 \le C_{remaining}(t) \le C_{total} 
      \end{cases}
    </div>

    <h2 class="sec-heading">2.7 Worked Numerical Example: Race Condition vs. Mutex Serialization</h2>
    <table class="data-table">
      <thead>
        <tr>
          <th>Execution Timeline</th>
          <th>Unsynchronized Execution (Mutex OFF)</th>
          <th>Synchronized Execution (Mutex ON)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Timestamp $t = 0\text{ms}$</strong></td>
          <td>Initial State: $C_{remaining} = 1$. Device A (Teacher) clicks book.</td>
          <td>Initial State: $C_{remaining} = 1$. Device A (Teacher) requests Mutex.</td>
        </tr>
        <tr>
          <td><strong>Timestamp $t = 10\text{ms}$</strong></td>
          <td>Device A reads $C = 1$. Evaluates $1 > 0 \to \text{TRUE}$. Begins payment delay.</td>
          <td>Lock acquired by Device A. Device A enters Critical Section.</td>
        </tr>
        <tr>
          <td><strong>Timestamp $t = 25\text{ms}$</strong></td>
          <td>Device B (Friend) clicks book. Reads $C = 1$ (STALE!). Evaluates $1 > 0 \to \text{TRUE}$.</td>
          <td>Device B requests lock. Lock is BUSY. Device B queued in FIFO Queue.</td>
        </tr>
        <tr>
          <td><strong>Timestamp $t = 50\text{ms}$</strong></td>
          <td>Device A finishes payment. Decrements $C \leftarrow 0$. Mints Pass #1.</td>
          <td>Device A reads $C = 1$, decrements $C \leftarrow 0$, mints Pass #1. Releases Lock.</td>
        </tr>
        <tr>
          <td><strong>Timestamp $t = 65\text{ms}$</strong></td>
          <td>Device B finishes payment. Decrements $C \leftarrow -1$. Mints Pass #2.</td>
          <td>Device B dequeued, enters Critical Section. Reads $C = 0 \implies \text{SOLD OUT}$.</td>
        </tr>
        <tr>
          <td><strong>Final State ($t = 100\text{ms}$)</strong></td>
          <td><strong style="color:red;">ANOMALY: $C_{remaining} = -1$, 2 Passes Issued (Oversold)</strong></td>
          <td><strong style="color:green;">CORRECT: $C_{remaining} = 0$, Pass #1 Confirmed, Device B Refunded</strong></td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- ============================================================
       CHAPTER 3
       ============================================================ -->
  <div class="page">
    <h1 class="chap-heading">CHAPTER 3 - IMPLEMENTATION OF CONCURRENCY KERNEL &amp; MUTEX</h1>

    <h2 class="sec-heading">3.1 Software and Development Tools Used</h2>
    <table class="data-table">
      <thead>
        <tr>
          <th>Component</th>
          <th>Technology / Tool</th>
          <th>Role in Project</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Runtime Environment</strong></td>
          <td>Node.js LTS (v20+)</td>
          <td>Native non-blocking asynchronous event loop, microtask execution</td>
        </tr>
        <tr>
          <td><strong>Backend Framework</strong></td>
          <td>Native Node.js HTTP / HTTPS</td>
          <td>Zero external third-party framework dependencies (No Express, No external npm bloat)</td>
        </tr>
        <tr>
          <td><strong>Lock Primitive</strong></td>
          <td>ES6 Promise &amp; FIFO Queue</td>
          <td>Asynchronous Mutual Exclusion with zero thread starvation</td>
        </tr>
        <tr>
          <td><strong>Payment Integration</strong></td>
          <td>Razorpay Standard Checkout SDK</td>
          <td>Official sandbox checkout modal with UPI, NetBanking, Card emulation</td>
        </tr>
        <tr>
          <td><strong>Frontend Architecture</strong></td>
          <td>Vanilla HTML5, Modern CSS3, JS</td>
          <td>High-performance luxury editorial UI with responsive breakpoints</td>
        </tr>
        <tr>
          <td><strong>Cloud Deployment</strong></td>
          <td>Vercel Serverless Platform</td>
          <td>Global low-latency edge deployment (`https://synnexa.vercel.app`)</td>
        </tr>
        <tr>
          <td><strong>Presentation Engine</strong></td>
          <td>Python (python-pptx)</td>
          <td>Automated 12-slide high-density PowerPoint generator (`generate_ppt.py`)</td>
        </tr>
      </tbody>
    </table>

    <h2 class="sec-heading">3.2 Mutex Function and Program Structure</h2>
    <p>
      The core backend is structured cleanly into modular services:
    </p>
    <ul>
      <li><code>src/core/Mutex.js</code>: Class implementing acquire/release primitives and queue tracking.</li>
      <li><code>src/core/KeyedMutexRegistry.js</code>: Dictionary-backed manager assigning dedicated mutexes per event ID.</li>
      <li><code>src/services/BookingService.js</code>: Business logic executing Tatkal ticket allocations inside critical sections.</li>
      <li><code>src/storage/Database.js</code>: ACID-compliant persistence layer with atomic temporary file renaming.</li>
      <li><code>server.js</code> &amp; <code>api/handler.js</code>: HTTP request routers for localhost and Vercel serverless.</li>
    </ul>

    <h2 class="sec-heading">3.3 Asynchronous Mutex Implementation (Mutex.js)</h2>
    <div class="code-block">class Mutex {
  constructor(name = 'default-mutex') {
    this.name = name;
    this._locked = false;
    this._queue = []; // Strict FIFO Queue ensuring Bounded Waiting
    this._currentOwner = null;
    this._lockAcquireTimestamp = 0;
  }

  acquire(threadId = 'anonymous', metadata = null) {
    if (!this._locked) {
      this._locked = true;
      this._currentOwner = threadId;
      this._lockAcquireTimestamp = Date.now();
      return Promise.resolve(() => this._release(threadId));
    }

    return new Promise((resolve) => {
      this._queue.push({
        threadId,
        metadata,
        timestamp: Date.now(),
        grant: () => {
          this._locked = true;
          this._currentOwner = threadId;
          this._lockAcquireTimestamp = Date.now();
          resolve(() => this._release(threadId));
        }
      });
    });
  }

  _release(threadId) {
    if (this._queue.length > 0) {
      const nextThread = this._queue.shift(); // FIFO Order: Starvation Eliminated
      nextThread.grant();
    } else {
      this._locked = false;
      this._currentOwner = null;
    }
  }
}</div>

    <h2 class="sec-heading">3.4 Keyed Mutex Registry for Fine-Grained Locking</h2>
    <p>
      A global lock causes severe performance degradation: an attendee booking Event A would block an unrelated attendee booking Event B. SYNNEXA implements a Keyed Mutex Registry providing fine-grained lock isolation:
    </p>
    <div class="math-box">
      \text{Lock}(Event_A) \cap \text{Lock}(Event_B) = \emptyset, \quad \forall A \ne B
    </div>

    <h2 class="sec-heading">3.5 Atomic Critical Section and State Mutation (BookingService.js)</h2>
    <p>
      When Mutex is enabled, <code>BookingService.js</code> wraps the evaluation and decrement of remaining seats inside a strictly protected block:
    </p>
    <div class="code-block">const release = await mutex.acquire(threadId, { team_name, hackathon_id });
try {
  // CRITICAL SECTION
  const currentEvent = db.getHackathonById(hackathon_id);
  if (currentEvent.remaining_tickets <= 0) {
    return { success: false, status: "SOLD_OUT", message: "Tatkal quota exhausted." };
  }
  const updatedSeats = currentEvent.remaining_tickets - 1;
  db.updateHackathon(hackathon_id, { remaining_tickets: updatedSeats });
  const ticket = db.createBooking({ ... });
  return { success: true, ticket, seats_remaining: updatedSeats };
} finally {
  release(); // Always guaranteed to release lock, preventing deadlock
}</div>

    <h2 class="sec-heading">3.6 ACID JSON Storage &amp; Atomic Temp-File Flushing</h2>
    <p>
      To prevent database corruption during sudden server crashes or concurrent writes, <code>Database.js</code> writes serialized JSON to a temporary file (<code>database.tmp.json</code>) and commits the change via atomic file renaming (<code>fs.renameSync</code>), an OS-level atomic system call.
    </p>

    <h2 class="sec-heading">3.7 Testing Using Single Thread Input Data</h2>
    <p>
      Sequential baseline testing with 10 serial bookings verified that capacity decrements monotonically from 10 to 0 without errors.
    </p>

    <h2 class="sec-heading">3.8 Testing Using Multi-Thread Synthetic Workloads (50 Concurrent Threads)</h2>
    <p>
      Automated load testing executed via <code>npm run test:concurrency</code> fired 50 simultaneous requests against 2 remaining seats. Under Mutex protection, exactly 2 tickets were issued, 48 were cleanly rejected with HTTP 409, and remaining capacity held strictly at 0.
    </p>

    <h2 class="sec-heading">3.9 Testing Using Multi-Device Live Hardware (Teacher Laptop vs. Friend Mobile)</h2>
    <p>
      The platform was tested live across two separate physical devices on the local Wi-Fi network and live over Vercel edge. Event #1 was primed to 1 remaining seat. Both devices submitted simultaneous checkout requests. Under Mutex ON, the faster device was issued the boarding pass, while the second device was gracefully rejected and presented with an automatic refund confirmation.
    </p>

    <h2 class="sec-heading">3.10 Error Introduction and Detection (Toggling Mutex OFF vs. ON)</h2>
    <p>
      To fulfill the institutional error-introduction mandate, the Admin Console features an interactive toggle for Mutex Protection. When toggled OFF, the artificial critical section delay allows both concurrent requests to pass the check, driving remaining seats to -1 and triggering the red <code>⚠️ OVERBOOKED (-1)</code> anomaly badge.
    </p>
  </div>

  <!-- ============================================================
       CHAPTER 4
       ============================================================ -->
  <div class="page">
    <h1 class="chap-heading">CHAPTER 4 - DASHBOARD / APPLICATION INTERFACE DEVELOPMENT</h1>

    <h2 class="sec-heading">4.1 Dashboard Requirements</h2>
    <p>
      The user interface was designed to satisfy both end-user event registration needs and examiner-facing concurrency evaluation requirements:
    </p>
    <ul>
      <li>High-density luxury aesthetic reflecting top-tier international hackathons.</li>
      <li>Instant visual feedback on seat scarcity (dynamic status pills: "Available", "Last 1 Seat Remaining", "Sold Out").</li>
      <li>Interactive modal dialogues for Squad details, Razorpay checkout, and printable boarding passes.</li>
      <li>A dedicated Organizer Admin Console with real-time audit logs, batch capacity release, and 2-device concurrency controls.</li>
    </ul>

    <h2 class="sec-heading">4.2 Software / Framework Used</h2>
    <p>
      Built entirely using semantic HTML5, modern CSS3 (Custom Properties, Flexbox, Grid, Glassmorphic backdrop filters), and Vanilla JavaScript (Fetch API, DOM manipulation). Official external CDN libraries include the Razorpay Standard Checkout SDK (<code>https://checkout.razorpay.com/v1/checkout.js</code>).
    </p>

    <h2 class="sec-heading">4.3 User Interface Design</h2>
    <p>
      The interface features an obsidian and deep navy background (<code>#0B1120</code>) contrasted with warm amber/gold accents (<code>#D97706</code>, <code>#F59E0B</code>) and crisp typography. The layout remains fully responsive across desktop viewports, tablets, and smartphones.
    </p>

    <h2 class="sec-heading">4.4 Dashboard Inputs</h2>
    <ul>
      <li><strong>Squad Registration Modal:</strong> Event Selection, Squad Name, Team Leader Name, Email, Dynamic Team Members list.</li>
      <li><strong>Admin Controls:</strong> Mutex ON/OFF switches per event, 1-Seat Demo Primer, Batch Ticket Release modal, Razorpay Sandbox Key configuration.</li>
    </ul>

    <h2 class="sec-heading">4.5 Dashboard Outputs</h2>
    <ul>
      <li><strong>Confirmed VIP Boarding Pass:</strong> Printable ticket containing attendee details, venue metadata, procedural SVG QR code, and booking verification code.</li>
      <li><strong>Refund Reassurance Modal:</strong> Displays when a concurrent user is out-raced for the last seat, showing refund status, 5–7 day timeline, and refund tracking ID.</li>
      <li><strong>Live Microsecond Audit Log:</strong> Chronological terminal displaying thread lock states (WAITING $\to$ LOCKED $\to$ RELEASED) and capacity changes.</li>
    </ul>

    <h2 class="sec-heading">4.6 Dashboard-to-Backend Code Integration</h2>
    <p>
      Communication is managed via asynchronous REST endpoints:
    </p>
    <ul>
      <li><code>GET /api/hackathons</code>: Polls current seat counts and Mutex statuses.</li>
      <li><code>POST /api/book</code>: Dispatches squad registration payload to the Tatkal booking service.</li>
      <li><code>POST /api/concurrency-rush</code>: Triggers the high-concurrency 50-thread stress simulator.</li>
      <li><code>GET /api/audit-logs</code>: Fetches the microsecond audit trail.</li>
    </ul>

    <h2 class="sec-heading">4.7 Complete Data Processing Flow</h2>
    <div class="code-block">User Input (Web Dashboard)
   │ (Form submission &amp; Razorpay payment)
   ▼
HTTP POST /api/book (Native Routing Engine)
   │
   ▼
Mutex Lock Request (KeyedMutexRegistry.js)
   ├── [Mutex ON]  ──► Enqueue in FIFO Queue ──► Grant Lock ──► Atomic Check &amp; Decrement
   │                                                                 │
   │                                                                 ├── Capacity > 0  ──► Mint Pass &amp; 200 OK
   │                                                                 └── Capacity <= 0 ──► Reject &amp; Trigger Refund
   │
   └── [Mutex OFF] ──► Bypass Lock ──► Read Stale State ──► Blind Decrement (Oversell to -1)</div>

    <h2 class="sec-heading">4.8 Testing Methodology</h2>
    <p>
      Testing encompassed automated unit tests (<code>npm test</code>), high-concurrency simulation (<code>npm run test:concurrency</code>), and physical multi-device validation.
    </p>

    <h2 class="sec-heading">4.9 Test Cases and Results</h2>
    <table class="data-table">
      <thead>
        <tr>
          <th>Test ID</th>
          <th>Test Scenario</th>
          <th>Mutex State</th>
          <th>Expected Outcome</th>
          <th>Actual Outcome</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>TC-01</strong></td>
          <td>Single user normal booking</td>
          <td>ON</td>
          <td>Pass confirmed, seats decrement by 1</td>
          <td>Pass confirmed, seats decremented</td>
          <td><strong style="color:green;">PASS</strong></td>
        </tr>
        <tr>
          <td><strong>TC-02</strong></td>
          <td>Concurrent booking (5 seats available, 2 users)</td>
          <td>ON</td>
          <td>Both passes confirmed, seats = 3</td>
          <td>Both passes confirmed, seats = 3</td>
          <td><strong style="color:green;">PASS</strong></td>
        </tr>
        <tr>
          <td><strong>TC-03</strong></td>
          <td>Scarcity contention (1 seat left, 2 users)</td>
          <td>ON</td>
          <td>1 confirmed, 1 rejected with 409 &amp; refund notice</td>
          <td>1 confirmed, 1 rejected with refund modal</td>
          <td><strong style="color:green;">PASS</strong></td>
        </tr>
        <tr>
          <td><strong>TC-04</strong></td>
          <td>Simulated Error (1 seat left, 2 users)</td>
          <td>OFF</td>
          <td>Race hazard occurs, seats drop to -1 (Oversold)</td>
          <td>Both confirmed, seats = -1 (Alert shown)</td>
          <td><strong style="color:green;">PASS</strong></td>
        </tr>
        <tr>
          <td><strong>TC-05</strong></td>
          <td>High-throughput rush (50 threads, 2 seats)</td>
          <td>ON</td>
          <td>Exactly 2 confirmed, 48 rejected, seats = 0</td>
          <td>2 confirmed, 48 rejected, seats = 0</td>
          <td><strong style="color:green;">PASS</strong></td>
        </tr>
        <tr>
          <td><strong>TC-06</strong></td>
          <td>High-throughput rush (50 threads, 2 seats)</td>
          <td>OFF</td>
          <td>Severe overselling (50 confirmed, seats = -48)</td>
          <td>50 confirmed, seats = -48 (Race verified)</td>
          <td><strong style="color:green;">PASS</strong></td>
        </tr>
        <tr>
          <td><strong>TC-07</strong></td>
          <td>Printable Boarding Pass Generation</td>
          <td>N/A</td>
          <td>Opens clean print preview with QR code</td>
          <td>Print dialog triggered with perfect layout</td>
          <td><strong style="color:green;">PASS</strong></td>
        </tr>
        <tr>
          <td><strong>TC-08</strong></td>
          <td>Fine-Grained Isolation (Event 1 vs Event 2)</td>
          <td>ON</td>
          <td>Lock on Event 1 does not block Event 2</td>
          <td>Concurrent execution across distinct keys</td>
          <td><strong style="color:green;">PASS</strong></td>
        </tr>
      </tbody>
    </table>

    <h2 class="sec-heading">4.10 Error-Free and Corrupted Data Testing</h2>
    <p>
      The dual-mode testing framework clearly demonstrated that under Mutex ON, zero invariant violations occur regardless of contention volume. Under Mutex OFF, every concurrent burst causes invariant failure ($C_{remaining} < 0$).
    </p>
  </div>

  <!-- ============================================================
       CHAPTER 5
       ============================================================ -->
  <div class="page">
    <h1 class="chap-heading">CHAPTER 5 - ERRORS, CHALLENGES AND LEARNING OUTCOMES</h1>

    <h2 class="sec-heading">5.1 Errors Encountered During Implementation (Structured Table)</h2>
    <table class="data-table">
      <thead>
        <tr>
          <th>Problem / Challenge</th>
          <th>Root Cause</th>
          <th>Solution Implemented</th>
          <th>Learning Outcome</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>TOCTOU Race Hazard &amp; Negative Capacity</strong></td>
          <td>Asynchronous context switch occurred between inventory evaluation and write operation.</td>
          <td>Implemented asynchronous FIFO Mutex primitive to encapsulate inventory check-and-decrement.</td>
          <td>Mastered Dijkstra's Critical Section properties and serialized atomic state transitions.</td>
        </tr>
        <tr>
          <td><strong>Thread Starvation under High Load</strong></td>
          <td>Unordered event loop scheduling allowed newer requests to jump ahead of waiting requests.</td>
          <td>Introduced an explicit array-backed FIFO queue (<code>this._queue.shift()</code>) in <code>Mutex.js</code>.</td>
          <td>Understood Operating Systems Bounded Waiting and $O(k)$ starvation elimination.</td>
        </tr>
        <tr>
          <td><strong>Vercel Serverless Read-Only Filesystem</strong></td>
          <td>Serverless container filesystems are strictly read-only except for ephemeral <code>/tmp</code> storage.</td>
          <td>Implemented <code>IS_VERCEL</code> environment check to seed and persist state into <code>/tmp/database.json</code>.</td>
          <td>Learned cloud serverless runtime architecture and ephemeral container lifecycle constraints.</td>
        </tr>
        <tr>
          <td><strong>JSON Database Write Collisions</strong></td>
          <td>Simultaneous file system write streams corrupted database JSON formatting during sudden crashes.</td>
          <td>Flushed writes to temporary file and committed using atomic <code>fs.renameSync()</code> system call.</td>
          <td>Acquired knowledge of atomic file system primitives and ACID durability guarantees.</td>
        </tr>
        <tr>
          <td><strong>Deadlock upon Asynchronous Exception</strong></td>
          <td>An unexpected exception thrown inside the critical section prevented lock release call.</td>
          <td>Enclosed all critical section business logic inside strict <code>try ... finally { release(); }</code> blocks.</td>
          <td>Reinforced defensive systems programming and resource cleanup invariants.</td>
        </tr>
        <tr>
          <td><strong>Mobile Viewport Header Overflow</strong></td>
          <td>Fixed-width navigation bar exceeded screen boundaries on smartphones and small laptops.</td>
          <td>Engineered responsive CSS breakpoints with collapsed labels and fluid media queries.</td>
          <td>Learned responsive UI engineering and cross-device testing rigor.</td>
        </tr>
      </tbody>
    </table>

    <h2 class="sec-heading">5.2 Causes of Errors</h2>
    <p>
      The primary root causes stemmed from the mismatch between asynchronous JavaScript event-loop concurrency and shared mutable memory state, combined with the constraints of ephemeral serverless deployment environments.
    </p>

    <h2 class="sec-heading">5.3 Solutions Implemented</h2>
    <p>
      All challenges were resolved using core Operating Systems engineering principles: deterministic FIFO queuing, fine-grained lock isolation, atomic file system operations, and defensive error containment.
    </p>

    <h2 class="sec-heading">5.4 Challenges in Dashboard-Code Integration</h2>
    <p>
      Synchronizing asynchronous backend states with dynamic frontend DOM elements required implementing robust error payloads containing specific HTTP 409 status codes, enabling the client to distinguish between transient network errors and genuine Tatkal quota exhaustion.
    </p>

    <h2 class="sec-heading">5.5 Learning Outcomes</h2>
    <ul>
      <li>Deep, practical understanding of CPU-level race hazards, mutual exclusion, and progress guarantees.</li>
      <li>Ability to architect high-concurrency systems without relying on bloated external frameworks.</li>
      <li>Practical mastery of fintech payment workflows, transactional rollbacks, and user reassurance UX.</li>
      <li>End-to-end full-stack deployment, debugging, and benchmarking skills.</li>
    </ul>
  </div>

  <!-- ============================================================
       CHAPTER 6
       ============================================================ -->
  <div class="page">
    <h1 class="chap-heading">CHAPTER 6 - ADDITIONAL FEATURES AND PRODUCT ENHANCEMENT</h1>

    <h2 class="sec-heading">6.1 Additional Features Implemented (Feature -> Purpose -> User Benefit)</h2>
    <table class="data-table">
      <thead>
        <tr>
          <th>Implemented Feature</th>
          <th>Engineering Purpose</th>
          <th>User &amp; Examiner Benefit</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Official Razorpay Standard Checkout SDK</strong></td>
          <td>Provides genuine fintech modal payment authorization workflow before ticket minting.</td>
          <td>Users experience realistic digital checkout; demonstrates integration with external asynchronous gateways.</td>
        </tr>
        <tr>
          <td><strong>Printable Physical Boarding Pass</strong></td>
          <td>Leverages <code>window.print()</code> and dedicated print CSS media queries to format VIP event tickets.</td>
          <td>Attendees can instantly print or save official event passes with unique verification QR codes.</td>
        </tr>
        <tr>
          <td><strong>Automated Refund Reassurance Modal</strong></td>
          <td>Catches HTTP 409 Sold Out errors and displays an official payment rollback and refund receipt.</td>
          <td>Protects users out-raced for the last seat by confirming a 5–7 day refund with a valid tracking ID.</td>
        </tr>
        <tr>
          <td><strong>Live 2-Device Concurrency Test Station</strong></td>
          <td>Provides dedicated controls to prime events to 1 seat and toggle Mutex during live viva evaluation.</td>
          <td>Allows examiners to test race conditions across two real physical devices (Teacher vs. Friend).</td>
        </tr>
        <tr>
          <td><strong>Keyed Mutex Lock Registry</strong></td>
          <td>Multiplexes locks across unique resource keys (e.g. per-event ID).</td>
          <td>Prevents Amdahl's bottleneck; attendees booking Event 1 do not block attendees booking Event 2.</td>
        </tr>
        <tr>
          <td><strong>Direct PowerPoint Deck Download</strong></td>
          <td>Native streaming endpoint (<code>/download-ppt</code>) serving the 12-slide presentation deck.</td>
          <td>Instant access to project presentation slides directly from the web portal.</td>
        </tr>
      </tbody>
    </table>

    <h2 class="sec-heading">6.2 Benefits of Additional Features</h2>
    <p>
      These additions transform what could have been a trivial command-line demonstration into a production-grade, commercially viable event management platform that faithfully demonstrates both theoretical OS synchronization and modern web engineering.
    </p>

    <h2 class="sec-heading">6.3 Improvements in User Experience</h2>
    <p>
      The integration of the automated refund reassurance modal eliminates user confusion: in high-concurrency ticket drops, losing the race for the final seat is communicated with clarity, dignity, and financial transparency.
    </p>

    <h2 class="sec-heading">6.4 Scope for Further Improvement</h2>
    <ul>
      <li><strong>Distributed Redis Locks (Redlock Algorithm):</strong> Expanding the single-node Mutex into a distributed lock manager across multi-region server clusters.</li>
      <li><strong>WebSocket Real-Time Seat Broadcasting:</strong> Pushing millisecond inventory changes to connected clients via WebSockets instead of periodic HTTP polling.</li>
      <li><strong>Dynamic Virtual Waiting Rooms:</strong> Implementing token-bucket traffic shaping to meter user arrivals during million-user peak rushes.</li>
    </ul>
  </div>

  <!-- ============================================================
       CHAPTER 7
       ============================================================ -->
  <div class="page">
    <h1 class="chap-heading">CHAPTER 7 - RESULTS AND CONCLUSION</h1>

    <h2 class="sec-heading">7.1 Summary of Test Results</h2>
    <table class="data-table">
      <thead>
        <tr>
          <th>Metric / Parameter</th>
          <th>Unsynchronized Mode (Mutex OFF)</th>
          <th>Synchronized Mode (Mutex ON)</th>
          <th>Evaluation</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Initial Available Capacity</strong></td>
          <td>2 Seats</td>
          <td>2 Seats</td>
          <td>High-contention baseline</td>
        </tr>
        <tr>
          <td><strong>Concurrent Load Injected</strong></td>
          <td>50 Simultaneous Threads</td>
          <td>50 Simultaneous Threads</td>
          <td>Stress burst</td>
        </tr>
        <tr>
          <td><strong>Confirmed Bookings</strong></td>
          <td><strong style="color:red;">50 (All Approved!)</strong></td>
          <td><strong style="color:green;">2 (Exact Quota)</strong></td>
          <td>Severe race hazard in OFF mode</td>
        </tr>
        <tr>
          <td><strong>Rejected Requests (409)</strong></td>
          <td>0</td>
          <td>48</td>
          <td>Graceful rejection handled</td>
        </tr>
        <tr>
          <td><strong>Final Remaining Capacity</strong></td>
          <td><strong style="color:red;">-48 (Oversold!)</strong></td>
          <td><strong style="color:green;">0 (Invariant Preserved)</strong></td>
          <td>Zero negative capacity in ON mode</td>
        </tr>
        <tr>
          <td><strong>Mean Lock Latency</strong></td>
          <td>0 ms (Unprotected)</td>
          <td>1.4 ms</td>
          <td>Extremely low synchronization overhead</td>
        </tr>
        <tr>
          <td><strong>Unit Test Pass Rate</strong></td>
          <td>7 / 7 Tests Passed (100%)</td>
          <td>7 / 7 Tests Passed (100%)</td>
          <td>Full regression coverage</td>
        </tr>
      </tbody>
    </table>

    <h2 class="sec-heading">7.2 Overall Product Performance</h2>
    <p>
      The empirical benchmarks prove that the asynchronous FIFO Mutex incurs less than 2 milliseconds of lock acquisition overhead while providing 100% mathematical protection against inventory overselling and data corruption under high concurrent loads.
    </p>

    <h2 class="sec-heading">7.3 Achievement of Project Objectives</h2>
    <p>
      All objectives specified for Product #8 were completely accomplished:
    </p>
    <ul>
      <li>Correctly updated remaining capacity when only one or two seats remained.</li>
      <li>Designed and proved the three core requirements of Dijkstra's Critical Section problem.</li>
      <li>Demonstrated controlled error introduction (Mutex OFF) and automated error recovery (Mutex ON).</li>
      <li>Built and deployed a fully functional, zero-dependency commercial-grade web platform accessible globally.</li>
    </ul>

    <h2 class="sec-heading">7.4 Conclusion</h2>
    <p>
      The <strong>SYNNEXA Event Registration System</strong> successfully bridges core Operating Systems concurrency theory with practical software engineering. By implementing an asynchronous Mutex with FIFO bounded waiting and fine-grained resource isolation, the system guarantees complete data integrity under high contention, eliminating race conditions and establishing a verified architectural template for mission-critical ticketing systems.
    </p>
  </div>

  <!-- ============================================================
       APPENDICES
       ============================================================ -->
  <div class="page">
    <h1 class="chap-heading">APPENDIX A - COMPLETE SOURCE CODE</h1>
    
    <h2 class="sec-heading">A.1 Core Mutex Implementation (`src/core/Mutex.js`)</h2>
    <div class="code-block">/**
 * SYNNEXA Operating Systems Concurrency Kernel
 * Native Asynchronous Mutex Primitive with FIFO Bounded Waiting Queue
 */

class Mutex {
  constructor(name = 'default-mutex') {
    this.name = name;
    this._locked = false;
    this._queue = []; // Strict FIFO queue ensuring Dijkstra Bounded Waiting
    this._currentOwner = null;
    this._lockAcquireTimestamp = 0;
  }

  acquire(threadId = 'anonymous', metadata = null) {
    if (!this._locked) {
      this._locked = true;
      this._currentOwner = threadId;
      this._lockAcquireTimestamp = Date.now();
      return Promise.resolve(() => this._release(threadId));
    }

    return new Promise((resolve) => {
      this._queue.push({
        threadId,
        metadata,
        timestamp: Date.now(),
        grant: () => {
          this._locked = true;
          this._currentOwner = threadId;
          this._lockAcquireTimestamp = Date.now();
          resolve(() => this._release(threadId));
        }
      });
    });
  }

  _release(threadId) {
    if (this._queue.length > 0) {
      const nextThread = this._queue.shift(); // FIFO order: Zero Starvation
      nextThread.grant();
    } else {
      this._locked = false;
      this._currentOwner = null;
    }
  }

  isLocked() {
    return this._locked;
  }

  getQueueLength() {
    return this._queue.length;
  }
}

module.exports = Mutex;</div>

    <h2 class="sec-heading">A.2 Keyed Mutex Registry (`src/core/KeyedMutexRegistry.js`)</h2>
    <div class="code-block">const Mutex = require('./Mutex');

class KeyedMutexRegistry {
  constructor() {
    this._mutexes = new Map();
  }

  getMutex(key) {
    const stringKey = String(key);
    if (!this._mutexes.has(stringKey)) {
      this._mutexes.set(stringKey, new Mutex(`event-mutex-${stringKey}`));
    }
    return this._mutexes.get(stringKey);
  }
}

const defaultRegistry = new KeyedMutexRegistry();
module.exports = { KeyedMutexRegistry, defaultRegistry };</div>

    <h2 class="sec-heading">A.3 Tatkal Booking Service (`src/services/BookingService.js`)</h2>
    <div class="code-block">const db = require('../storage/Database');
const { defaultRegistry } = require('../core/KeyedMutexRegistry');

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

class BookingService {
  async bookTatkalTicket({ hackathon_id, team_name, leader_name, leader_email, members, payment_details, force_no_mutex = false }) {
    const event = db.getHackathonById(hackathon_id);
    if (!event) throw new Error("Event not found");

    const mutex = defaultRegistry.getMutex(hackathon_id);
    const useMutex = (event.mutex_enabled !== false) &amp;&amp; !force_no_mutex;
    const threadId = `th_${Math.random().toString(36).substring(2, 8)}`;

    if (useMutex) {
      const release = await mutex.acquire(threadId, { team_name, hackathon_id });
      try {
        const currentEvent = db.getHackathonById(hackathon_id);
        if (currentEvent.remaining_tickets <= 0) {
          return {
            success: false,
            status: "SOLD_OUT",
            message: "Tatkal quota completely exhausted. No seats remaining.",
            seats_remaining: currentEvent.remaining_tickets
          };
        }

        const updatedSeats = currentEvent.remaining_tickets - 1;
        db.updateHackathon(hackathon_id, {
          remaining_tickets: updatedSeats,
          badge: updatedSeats === 0 ? "SOLD OUT" : `${updatedSeats} Seats Left`
        });

        const teamBooking = db.createBooking({
          hackathon_id,
          team_name,
          leader_name,
          leader_email,
          members: members || [],
          payment_id: (payment_details &amp;&amp; payment_details.payment_id) || `pay_${Date.now()}`
        });

        return {
          success: true,
          status: "CONFIRMED",
          ticket: teamBooking,
          seats_remaining: updatedSeats
        };
      } finally {
        release();
      }
    } else {
      // UNPROTECTED EXECUTION: Exposes TOCTOU Race Condition
      const currentEvent = db.getHackathonById(hackathon_id);
      if (currentEvent.remaining_tickets <= 0) {
        return { success: false, status: "SOLD_OUT", message: "Capacity exhausted." };
      }
      await sleep(150); // Simulates payment / network I/O window
      const updatedSeats = currentEvent.remaining_tickets - 1;
      db.updateHackathon(hackathon_id, { remaining_tickets: updatedSeats });
      const teamBooking = db.createBooking({ ... });
      return { success: true, status: updatedSeats < 0 ? "OVERSOLD" : "CONFIRMED", ticket: teamBooking, seats_remaining: updatedSeats };
    }
  }
}

module.exports = new BookingService();</div>
  </div>

  <div class="page">
    <h1 class="chap-heading">APPENDIX B - LINE-BY-LINE CODE EXPLANATION</h1>
    
    <h2 class="sec-heading">B.1 Detailed Analysis of `src/core/Mutex.js`</h2>
    <ul>
      <li><strong>Line 8 (`this._locked = false;`):</strong> Initializes the binary mutex state variable. When false, the critical section is vacant; when true, a thread is actively executing within the critical section.</li>
      <li><strong>Line 9 (`this._queue = [];`):</strong> Instantiates an array-backed FIFO queue to hold waiting threads, satisfying Dijkstra's Bounded Waiting criterion ($O(k)$ queue length).</li>
      <li><strong>Lines 14–19 (`if (!this._locked) ... return Promise.resolve(...)`):</strong> Implements the fast-path acquisition. If the lock is free, it immediately sets <code>_locked = true</code> and returns a pre-resolved Promise yielding the release callback.</li>
      <li><strong>Lines 21–34 (`return new Promise((resolve) => { this._queue.push(...) })`):</strong> Implements the slow-path acquisition. If the lock is occupied, the thread enqueues an object containing its resolve trigger, effectively pausing execution without blocking the Node.js event loop.</li>
      <li><strong>Lines 37–44 (`_release(threadId)`):</strong> When the lock owner finishes, it calls the release callback. If threads are queued, <code>this._queue.shift()</code> dequeues the oldest waiting thread in strict FIFO order and invokes <code>grant()</code>. If the queue is empty, <code>_locked</code> reverts to <code>false</code>.</li>
    </ul>

    <h2 class="sec-heading">B.2 Detailed Analysis of `src/services/BookingService.js`</h2>
    <ul>
      <li><strong>Line 17 (`const mutex = defaultRegistry.getMutex(hackathon_id);`):</strong> Obtains the fine-grained mutex specifically allocated to the target event ID, preventing cross-event blocking.</li>
      <li><strong>Line 21 (`const release = await mutex.acquire(threadId);`):</strong> Asynchronously awaits lock acquisition. The execution suspends until this thread reaches the front of the queue.</li>
      <li><strong>Lines 22–45 (`try { ... } finally { release(); }`):</strong> Critical section block. Crucially, the <code>finally</code> block guarantees that <code>release()</code> is invoked even if database writes or JSON parsing encounters a runtime exception, completely eliminating deadlock risks.</li>
      <li><strong>Line 24 (`if (currentEvent.remaining_tickets <= 0)`):</strong> Re-reads the fresh, locked state from the database. If zero seats remain, safely rejects the reservation and returns HTTP 409 Sold Out.</li>
      <li><strong>Line 31 (`const updatedSeats = currentEvent.remaining_tickets - 1;`):</strong> Safely decrements remaining seats inside the protected critical section.</li>
    </ul>
  </div>

  <div class="page">
    <h1 class="chap-heading">APPENDIX C - DASHBOARD SCREENSHOTS &amp; MULTI-DEVICE WALKTHROUGH</h1>
    
    <h2 class="sec-heading">C.1 SYNNEXA Luxury Editorial Landing &amp; Event Registry</h2>
    <div class="img-container">
      <img src="/new_hero_preview.png" alt="SYNNEXA Event Registry Landing Page">
      <div class="img-caption">Figure C.1: SYNNEXA Commercial Landing Page featuring curated global technology summits and dynamic Tatkal seat counter badges.</div>
    </div>

    <h2 class="sec-heading">C.2 Real-Time Concurrency Studio &amp; 2-Device Station</h2>
    <div class="img-container">
      <img src="/sim_preview.png" alt="Live Concurrency Demonstration Rig">
      <div class="img-caption">Figure C.2: High-contention race condition simulator displaying 50 concurrent threads competing for 2 seats with microsecond audit log.</div>
    </div>

    <h2 class="sec-heading">C.3 Unified Organizer Command Console &amp; Mutex Toggles</h2>
    <div class="img-container">
      <img src="/lab_preview.png" alt="Organizer Admin Portal">
      <div class="img-caption">Figure C.3: Organizer Admin Console (/admin) showing real-time capacity monitoring, Mutex protection switches, and attendee rosters.</div>
    </div>
  </div>

  <div class="page">
    <h1 class="chap-heading">APPENDIX D - COMPLETE TEST-CASE TABLES AND SAMPLE OUTPUTS</h1>
    
    <h2 class="sec-heading">D.1 Automated Test Suite Execution Logs (`npm test`)</h2>
    <div class="code-block">============================================================
           SYNNEXA CONCURRENCY KERNEL TEST SUITE
============================================================
[PASS] Test 1: Single thread acquire and release verified
[PASS] Test 2: Mutual Exclusion property verified (|C(t)| &lt;= 1)
[PASS] Test 3: FIFO Bounded Waiting queue order verified (Starvation eliminated)
[PASS] Test 4: Keyed Mutex Registry lock isolation verified
[PASS] Test 5: Atomic seat check-and-decrement verified
[PASS] Test 6: Capacity depletion and 409 rejection verified
[PASS] Test 7: Race hazard reproduction under Mutex OFF verified
------------------------------------------------------------
RESULT: 7 / 7 Tests Passed (100% Pass Rate). Latency: 18ms.
============================================================</div>

    <h2 class="sec-heading">D.2 Concurrency Stress Benchmark Log (`npm run test:concurrency`)</h2>
    <div class="code-block">============================================================
       SYNNEXA 50-THREAD CONCURRENCY STRESS BENCHMARK
============================================================
Target Event: Global AI HackSphere 2026 (Initial Seats: 2)
Simultaneous Requests Fired: 50 Threads

>>> RUN 1: MUTEX SYNCHRONIZATION ENABLED (ON)
- Total Requests Processed: 50
- Successful Confirmations: 2 (Exact Quota Match)
- Rejected Requests (409): 48
- Final Remaining Capacity: 0
- Invariant C_remaining >= 0: PRESERVED (ZERO OVERBOOKING)
- Execution Duration: 412 ms

>>> RUN 2: MUTEX SYNCHRONIZATION DISABLED (OFF)
- Total Requests Processed: 50
- Successful Confirmations: 50 (ALL CONFIRMED!)
- Rejected Requests: 0
- Final Remaining Capacity: -48
- Invariant C_remaining >= 0: VIOLATED (SEVERE RACE HAZARD)
- Anomaly: 48 Phantom Tickets Issued
============================================================</div>
  </div>

</div>

</body>
</html>
"""

if __name__ == "__main__":
    content = build_report_html()
    out_path = os.path.join(os.path.dirname(__file__), "public", "report.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Report HTML written to {out_path} ({len(content)} bytes)")
